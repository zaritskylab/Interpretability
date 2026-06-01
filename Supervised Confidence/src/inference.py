import os
import sys
import time
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import tifffile as tiff
from scipy.signal.windows import triang
from keras.models import load_model

from torchvision.models.video import r3d_18

import random
random.seed(42)


# Transformation functions-make into a class
def normalize_std(input_image):
    # Ensure input is a numpy array and convert to float64 for precision
    input_image = np.array(input_image, dtype=np.float64)

    # Calculate mean and standard deviation
    mean = np.mean(input_image)
    std = np.std(input_image)

    if (np.isnan(mean) or np.isnan(std) or np.isinf(mean) or np.isinf(std)):
        max_val = np.max(input_image[np.isfinite(input_image)])
        input_image = np.where(input_image == np.inf, max_val, input_image)
        mean = np.mean(input_image, dtype=np.float64)
        std = np.std(input_image, dtype=np.float64)

    # Check and adjust standard deviation to avoid division by zero
    if std == 0:
        std = 1  # Prevent division by zero; alternatively could use a very small number

    # Normalize the image
    normalized_image = (input_image - mean) / std

    # Replace NaN values that might result from zero divisions or infinite values in input
    normalized_image = np.nan_to_num(normalized_image, nan=0.0)

    return normalized_image


def get_weights(shape):
    """Generate a 3D triangular weighting mask for smooth patch blending."""
    shape_in = shape  # e.g., (1, 32, 128, 128, 1)
    shape = shape[1:-1]  # (D, H, W)
    
    # Start with ones of the right shape
    weights = np.ones(shape)
    
    for dim, size in enumerate(shape):
        axis_weights = triang(size)
        # Reshape axis_weights to broadcast across full shape
        reshape_dims = [1] * len(shape)
        reshape_dims[dim] = size
        axis_weights = axis_weights.reshape(reshape_dims)
        
        weights *= axis_weights  # Proper broadcasting multiplication

    # Add batch and channel dimensions back
    weights = weights[np.newaxis, ..., np.newaxis]  # shape: (1, D, H, W, 1)
    return weights.astype(np.float32)


def compute_padding(img_dim, patch_size, stride):
    full_coverage = ((img_dim - patch_size) + stride - 1) // stride * stride + patch_size
    total_pad = full_coverage - img_dim
    pad_before = total_pad // 2
    pad_after = total_pad - pad_before
    return pad_before, pad_after


class ResNet3DRegression(nn.Module):
    def __init__(self, fine_tune_layers='partial'):
        super(ResNet3DRegression, self).__init__()
        # Load pretrained 3D ResNet
        self.resnet3d = r3d_18(pretrained=True)

        # Adjust the first convolutional layer for single-channel input
        self.resnet3d.stem[0] = nn.Conv3d(
            in_channels=2,
            out_channels=64,
            kernel_size=(3, 7, 7),
            stride=(1, 2, 2),
            padding=(1, 3, 3),
            bias=False
        )

        self.resnet3d.fc = nn.Identity()  # Remove the classification head

        # Fully connected layers for regression
        self.fc1 = nn.Linear(512, 128)  # ResNet3D outputs 512 features
        self.fc2 = nn.Linear(128, 1)

        # Fine-tuning options
        if fine_tune_layers == 'fc_only':  # Train only fc1 and fc2
            for param in self.resnet3d.parameters():
                param.requires_grad = False
        elif fine_tune_layers == 'partial':  # Train fc1, fc2, and later layers (e.g., layer4)
            for name, param in self.resnet3d.named_parameters():
                if 'layer4' in name or 'fc' in name:
                    param.requires_grad = True
                else:
                    param.requires_grad = False
        elif fine_tune_layers == 'full':  # Train all layers
            for param in self.resnet3d.parameters():
                param.requires_grad = True

    def forward(self, x):
        x = self.resnet3d(x)  # Pass through 3D ResNet
        x = torch.relu(self.fc1(x))  # Fully connected layer 1
        # x = torch.nn.functional.softplus(self.fc2(x))  # Output layer
        x = torch.relu(self.fc2(x))  # Output layer
        return x


# Define base path for all operations
BASE_PATH = os.path.dirname(os.getcwd())

# Variable Paths
organelle = sys.argv[1]
unet_model_path = f"{BASE_PATH}/models/unet/{organelle}/"
mg_model_path = f"{BASE_PATH}/models/mg/{organelle}/"
conf_model_path = f"{BASE_PATH}/models/confidence/{organelle}/conf_model.pt"
test_csv_path = f"{BASE_PATH}/data/{organelle}/image_list_test.csv"

input_channel=0
if organelle == "DNA":
    target_channel=1
else:
    target_channel=3

# Load neccessary models
unet = load_model(unet_model_path)
mg = load_model(mg_model_path)
conf_model = ResNet3DRegression(fine_tune_layers='partial')
conf_model.load_state_dict(torch.load(conf_model_path, weights_only=True))
conf_model.eval()

# Patch settings
patch_size = [32, 128, 128]
stride_z = 16
stride_xy = 32

test_csv = pd.read_csv(test_csv_path)
save_folder = f"{BASE_PATH}/inference/{organelle}"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)
    
for path in test_csv['path_tiff']:
    path = path.replace('Interpretability/interpretability', "")
    path = BASE_PATH + '/' + path.split('//')[1]
    image = tiff.imread(path)
    image_num = path.split('.')[0].split('_')[-1]

    input_image = image[input_channel, :, :, :]
    Z, X, Y = input_image.shape
    
    target_image = image[target_channel, :, :, :]
    
    input_image = normalize_std(input_image)

    # Compute padding
    pad_z = compute_padding(Z, patch_size[0], stride_z)
    pad_x = compute_padding(X, patch_size[1], stride_xy)
    pad_y = compute_padding(Y, patch_size[2], stride_xy)
    
    # Pad input and target symmetrically
    input_padded = np.pad(input_image, (pad_z, pad_x, pad_y), mode='reflect')
    target_padded = np.pad(target_image, (pad_z, pad_x, pad_y), mode='reflect')
    
    # Update dimensions for loop
    Z_pad, X_pad, Y_pad = input_padded.shape

    # Initialize output volumes
    prediction = np.zeros_like(input_padded)
    importance_map = np.zeros_like(input_padded)
    confidence_map = np.zeros_like(input_padded)
    weight_sum = np.zeros_like(input_padded) + 1e-4

    # Slide over the full volume with overlap
    start = time.time()
    
    for i in range(0, Z_pad - patch_size[0] + 1, stride_z):
        for j in range(0, X_pad - patch_size[1] + 1, stride_xy):
            for k in range(0, Y_pad - patch_size[2] + 1, stride_xy):
                # Slice patch
                patch_input = input_padded[i:i+patch_size[0], j:j+patch_size[1], k:k+patch_size[2]]
                patch_target = target_padded[i:i+patch_size[0], j:j+patch_size[1], k:k+patch_size[2]]
    
                # Prepare for models (N, D, H, W, C)
                patch_input_tensor = np.expand_dims(patch_input, axis=(0, -1))  # shape: (1, D, H, W, 1)
                patch_target_tensor = np.expand_dims(patch_target, axis=(0, -1))  # shape: (1, D, H, W, 1)
    
                # ISL prediction
                patch_prediction = unet(patch_input_tensor)  # shape: (1, D, H, W, 1)
    
                # Importance mask
                patch_mask = mg.generator([patch_input_tensor, patch_prediction]).numpy()  # shape: (1, D, H, W, 1)
    
                # Combine for confidence model
                patch_combined = np.concatenate([patch_prediction, patch_mask], axis=-1)  # (1, D, H, W, 2)
                patch_combined = torch.from_numpy(patch_combined).float().permute(0, 4, 1, 2, 3)  # (1, 2, D, H, W)
    
                patch_confidence = conf_model(patch_combined)  # shape: (1, 1)
    
                # Get weights and accumulate predictions
                weights = get_weights(patch_prediction.shape)  # shape: (1, D, H, W, 1)
                patch_prediction_np = patch_prediction[0, ..., 0]  # Remove batch/channel → (D, H, W)
                patch_mask_np = patch_mask[0, ..., 0]  # shape: (D, H, W)
    
                # Broadcast scalar confidence value to patch shape
                confidence_patch = np.full_like(patch_prediction_np, patch_confidence.item())
    
                # Accumulate weighted predictions
                prediction[i:i+patch_size[0], j:j+patch_size[1], k:k+patch_size[2]] += patch_prediction_np * weights[0, ..., 0]
                importance_map[i:i+patch_size[0], j:j+patch_size[1], k:k+patch_size[2]] += patch_mask_np * weights[0, ..., 0]
                confidence_map[i:i+patch_size[0], j:j+patch_size[1], k:k+patch_size[2]] += confidence_patch * weights[0, ..., 0]
                weight_sum[i:i+patch_size[0], j:j+patch_size[1], k:k+patch_size[2]] += weights[0, ..., 0]
    
    end = time.time()
    print(f"Sliding window inference took {end - start:.2f} seconds.")

    # Normalize final maps
    prediction = prediction / weight_sum
    importance_map = importance_map / weight_sum
    confidence_map = confidence_map / weight_sum

    # Crop back to original shape
    z0, z1 = pad_z[0], Z_pad - pad_z[1]
    x0, x1 = pad_x[0], X_pad - pad_x[1]
    y0, y1 = pad_y[0], Y_pad - pad_y[1]

    prediction = prediction[z0:z1, x0:x1, y0:y1]
    importance_map = importance_map[z0:z1, x0:x1, y0:y1]
    confidence_map = confidence_map[z0:z1, x0:x1, y0:y1]

    # Stack into one (3, Z, X, Y) array
    stack = np.stack([prediction, importance_map, confidence_map], axis=0)
    tiff.imwrite(f"{save_folder}/image_{image_num}_inference_outputs.tiff", stack.astype(np.float32))
