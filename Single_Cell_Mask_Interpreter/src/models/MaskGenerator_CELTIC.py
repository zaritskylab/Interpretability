import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch.nn import MSELoss
from torch.cuda.amp import autocast, GradScaler

from src.metrics import pearson_corr_torch


class MaskGenerator(nn.Module):
    def __init__(self, patch_size, adaptor, celtic_wrapper, mask_loss_weight=0.8,
                 weighted_pcc=False, pcc_target=0.9, noise_scale=1.0):
        super(MaskGenerator, self).__init__()

        self.celtic_wrapper = celtic_wrapper
        self.adaptor = adaptor
        self.pcc_target = pcc_target
        self.mask_loss_weight = mask_loss_weight
        self.noise_scale = noise_scale
        self.weighted_pcc = weighted_pcc
        
        # Initialize scaler once (e.g., in __init__ or before training starts)
        self.scaler = GradScaler()


        in_channels = patch_size[-1] * 2
        self.mask_net = adaptor  # already accepts concatenated input (image + target)

        self.mse_loss = MSELoss()

    def forward(self, signal, context, target, m):
        # --- CELTIC prediction on-the-fly ---
        prediction = self.celtic_wrapper(signal, context, m)

        # --- Generator forward pass ---
        x_input = torch.cat([
        F.relu(F.conv3d(signal, weight=torch.ones(1, signal.shape[1], 3, 3, 3, device=signal.device), padding=1)),
        F.relu(F.conv3d(prediction, weight=torch.ones(1, prediction.shape[1], 3, 3, 3, device=signal.device), padding=1))
    ], dim=1)

        mask = self.mask_net(x_input)

        noise = torch.randn_like(mask) * self.noise_scale
        adapted_image = (mask * signal) + ((1 - mask) * noise)

        # unet_prediction = self.celtic_wrapper.predict(adapted_image[0].cpu().numpy(), context_np[0])
        unet_prediction = self.celtic_wrapper(adapted_image, context, m)

        # --- Loss calculations ---
        unet_loss = self.mse_loss(unet_prediction, prediction)
        mask_loss = self.mse_loss(mask, torch.zeros_like(mask))

        if self.weighted_pcc:
            pcc = pearson_corr_torch(unet_prediction, prediction, target)
        else:
            pcc = pearson_corr_torch(unet_prediction, prediction)

        pcc_penalty = (self.pcc_target - pcc).clamp(min=0).pow(2) * 10

        total_loss = (1 - self.mask_loss_weight) * unet_loss + self.mask_loss_weight * mask_loss + pcc_penalty
        print(f"UNET Loss: {unet_loss.item():.2f}, Mask Loss: {mask_loss.item():.2f}, PCC Penalty: {pcc_penalty.item():.2f}")

        return total_loss, mask, pcc

    def train_step(self, data, target, m, optimizer):
        self.train()
        optimizer.zero_grad()
    
        with autocast():
            loss, mask, pcc = self.forward(*data, target, m)
    
        # Scales the loss, calls backward(), and unscales gradients before step
        self.scaler.scale(loss).backward()
        self.scaler.step(optimizer)
        self.scaler.update()
    
        return {
            "total_loss": loss.item(),
            "pcc": pcc.item(),
        }

    # def train_step(self, data, target, optimizer):
    #     self.train()
    #     optimizer.zero_grad()
    #     loss, mask, pcc = self(*data, target)
    #     loss.backward()
    #     optimizer.step()
    #     return {
    #         "total_loss": loss.item(),
    #         "pcc": pcc.item(),
    #     }
    
    @torch.no_grad()
    def test_step(self, data, target, m):
        self.eval()
        loss, mask, pcc = self(*data, target, m)
        return {
            "val_loss": loss.item(),
            "val_pcc": pcc.item(),
        }
