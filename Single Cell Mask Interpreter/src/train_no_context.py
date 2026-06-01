import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
import sys

import json
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import pandas as pd
from torch.utils.data import DataLoader

project_root = os.path.abspath("..")
sys.path.append(project_root)

from src.dataset_no_context import DataGen
from src.models.MaskGenerator_No_Context import MaskGenerator
from src.models.UNETO_CELTIC import UNet3D
from src.models.fnet_model import CELTICModel
from src.transforms import normalize, normalize_with_mask, Propper


# --- Configuration ---
CONTINUE_TRAINING = True
weighted_pcc = False
signals_are_masked = True
organelle = sys.argv[1]

BASE_PATH = os.path.dirname(os.getcwd())
unet_model_path = f"{BASE_PATH}/models/unet/{organelle}/best_model_no_context.p"
mg_model_path = f"{BASE_PATH}/models/mg/{organelle}/model_no_context.pt"
data_path = f"{BASE_PATH}/data/{organelle}/cells"
train_csv_path = f"{BASE_PATH}/data/{organelle}/metadata/train_images.csv"
validation_csv_path = f"{BASE_PATH}/data/{organelle}/metadata/valid_images.csv"
patch_size = (32, 64, 64, 1)


class Wrapper(nn.Module):
    def __init__(self, celtic_model):
        super().__init__()
        self.model = celtic_model
        self.model.net.eval()
        for param in self.model.net.parameters():
            param.requires_grad = False  # Freeze weights

    def forward(self, signal: torch.Tensor, m = None):
        pred = self.model.net(signal)
        pred = pred * m
        return pred


class EarlyStopping:
    def __init__(self, patience=5, verbose=True, path=f"{mg_model_path}"):
        self.patience = patience
        self.verbose = verbose
        self.path = path
        self.counter = 0
        self.best_loss = float('inf')
        self.early_stop = False

    def __call__(self, val_loss, model):
        if val_loss < self.best_loss:
            self.best_loss = val_loss
            self.counter = 0
            self.save_checkpoint(model)
        else:
            self.counter += 1
            if self.verbose:
                print(f"[EarlyStopping] No improvement for {self.counter} epoch(s).")
            if self.counter >= self.patience:
                if self.verbose:
                    print("[EarlyStopping] Stopping training.")
                self.early_stop = True

    def save_checkpoint(self, model):
        if self.verbose:
            print(f"[EarlyStopping] Validation loss improved. Saving model to {self.path}")
        torch.save(model.state_dict(), self.path)


# --- Load context config ---
with open(f"{RESOURCES_PATH}/{organelle}/models/context_model_config.json", 'r') as file:
    context_model_config = json.load(file)

transforms_config = context_model_config["transforms"]

# Evaluate each string in the config using `eval`, injecting train_patch_size
transforms = {
    k: eval(v, {"normalize": normalize,
                "normalize_with_mask": normalize_with_mask,
                "Propper": Propper,
                "train_patch_size": patch_size[:-1]})
    for k, v in transforms_config.items()
}

# === Load Datasets ===
train_dataset = CELTICDataGen(train_csv_path, data_path, transforms, signals_are_masked)
val_dataset = CELTICDataGen(validation_csv_path, data_path, transforms, signals_are_masked)
train_loader = DataLoader(train_dataset, batch_size=1, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=1, shuffle=False)

context_features = context_model_config['context_features']
daft_embedding_factor = context_model_config['daft_embedding_factor']
daft_scale_activation = context_model_config['daft_scale_activation']

# --- Load CELTIC model ---
model = CELTICModel(context=None, signals_are_masked=signals_are_masked)
model.load_state(unet_model_path)
model_wrapper = CELTICWrapper(model)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.net.to(device)

unet = UNet3D(in_channels=2, out_channels=1)

for mw in [0.9]:
    for lr in [0.00001]:
        for pcc_target in [0.89]:
            for noise in [1.0]:
        
                mg = MaskGenerator(patch_size, unet, celtic_wrapper, mask_loss_weight=mw, weighted_pcc=weighted_pcc,
                                   pcc_target=pcc_target, noise_scale=noise)
                
                if CONTINUE_TRAINING and os.path.exists(f"{mg_model_path[:-3]}_mw_{mw}_lr_{lr}_pcc_{pcc_target}_noise_{noise}.pt"):
                    mg.load_state_dict(torch.load(f"{mg_model_path[:-3]}_mw_{mw}_lr_{lr}_pcc_{pcc_target}_noise_{noise}.pt",
                                                  map_location=device))
                
                # === Training Setup ===
                mg.to(device)
                num_epochs = 100
                optimizer = optim.Adam(mg.parameters(), lr=lr)
                
                early_stopper = EarlyStopping(path=f"{mg_model_path[:-3]}_mw_{mw}_lr_{lr}_pcc_{pcc_target}_noise_{noise}.pt")
                # early_stopper = EarlyStopping()
                
                print("Starting training...")
                for epoch in range(num_epochs):
                    mg.train()
                    for x, y, m in train_loader:
                        x, y, m = x.to(device), y.to(device), m.to(device)
                        loss_dict = mg.train_step(x, y, m, optimizer)
                    print(f"Epoch {epoch}: {loss_dict}")
                
                    mg.eval()
                    # val_losses = []
                    with torch.no_grad():
                        for x, y, m in val_loader:
                            x, y, m = x.to(device), y.to(device), m.to(device)
                            val_loss_dict = mg.test_step(x, y, m)
                            # val_losses.append(val_loss_dict["val_loss"])
                    # avg_val_loss = sum(val_losses) / len(val_losses)
                    print(f"Validation: {val_loss_dict}")
                
                    early_stopper(val_loss_dict["val_loss"], mg)
                    if early_stopper.early_stop:
                        break
                
                print("Training complete.")
