import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import pandas as pd
import numpy as np
import math
import tifffile as tiff
import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2

from torchvision.models.video import r3d_18

import random
random.seed(42)


def tf_pearson_corr_aux(x,y):
    mean_x = tf.reduce_mean(x)
    mean_y = tf.reduce_mean(y)
    std_x = tf.math.reduce_std(x-mean_x)
    std_y = tf.math.reduce_std(y-mean_y)
    cc = tf.reduce_mean((x - mean_x) * (y - mean_y)) / (std_x * std_y)
    return cc


def tf_pearson_corr(y_true, y_pred, weights=None):
    if weights is not None:
        ind = tf.where(tf.logical_or(tf.reshape(weights,[-1])==1.0,tf.reshape(weights,[-1])==255.0))
        non_ind = tf.where(tf.logical_and(tf.reshape(weights,[-1])!=1.0,tf.reshape(weights,[-1])!=255.0))
        cc = 0
        t_weights = [1.0,0.0]
        t = [ind,non_ind]
        for i in range(2):
            [x,y] = tf.cond(tf.shape(ind)[0]>0, lambda: [tf.gather(tf.reshape(y_true,[-1]), t[i]),tf.gather(tf.reshape(y_pred,[-1]), t[i])], lambda: [y_true,y_pred])
            cc = cc + t_weights[i]*tf_pearson_corr_aux(x,y)
    else:
        x = y_true
        y = y_pred
        cc = tf_pearson_corr_aux(x,y)
    return cc


# Helper Functions
def get_random_patch(image, gt, patch_size=(32, 128, 128)):
    # Ensure the images are large enough for the patch size
    assert image.shape[0] >= patch_size[0], "Patch size is too large for the given z-dimension."
    assert image.shape[1] >= patch_size[1] and image.shape[2] >= patch_size[
        2], "Patch size is too large for the given image dimensions."

    # Calculate the maximum starting points for the random patch along each axis
    max_z = image.shape[0] - patch_size[0]  # z-axis (depth)
    max_x = image.shape[1] - patch_size[1]  # x-axis (height)
    max_y = image.shape[2] - patch_size[2]  # y-axis (width)

    # Generate random start points along each axis
    start_z = np.random.randint(0, max_z)
    start_x = np.random.randint(0, max_x)
    start_y = np.random.randint(0, max_y)

    # Extract the 3D patch from the image and the ground truth (gt)
    patch = image[start_z:start_z + patch_size[0], start_x:start_x + patch_size[1], start_y:start_y + patch_size[2]]
    gt_patch = gt[start_z:start_z + patch_size[0], start_x:start_x + patch_size[1], start_y:start_y + patch_size[2]]

    return patch, gt_patch


def get_patch(image, gt, sx, sy, patch_size=(32, 128, 128)):
    # Ensure the images are large enough for the patch size
    assert image.shape[0] >= patch_size[0], "Patch size is too large for the given z-dimension."
    assert image.shape[1] >= patch_size[1] and image.shape[2] >= patch_size[
        2], "Patch size is too large for the given image dimensions."

    # Extract the 3D patch from the image and the ground truth (gt)
    patch = image[16:48, sx:sx + patch_size[1], sy:sy + patch_size[2]]
    gt_patch = gt[16:48, sx:sx + patch_size[1], sy:sy + patch_size[2]]

    return patch, gt_patch


def calculate_iou(i1, i2):
    tp = np.logical_and(i1, i2)
    fp = np.subtract(np.logical_or(i1, i2), i1)
    fn = np.subtract(np.logical_or(i1, i2), i2)
    if float((tp.sum() + fp.sum() + fn.sum())) == 0:
        return 0
    iou_score = float(tp.sum()) / float((tp.sum() + fp.sum() + fn.sum()))
    return float(iou_score)


def calculate_pcc(image1, image2):
    if image1.shape != image2.shape:
        raise ValueError("Images must have the same dimensions for correlation calculation.")

    # Flatten the images to 1D arrays
    image1_flat = image1.ravel()
    image2_flat = image2.ravel()

    # Compute the Pearson correlation coefficient matrix
    correlation_matrix = np.corrcoef(image1_flat, image2_flat)

    # The Pearson correlation coefficient is in position [0, 1] of the matrix
    pcc = correlation_matrix[0, 1]
    return pcc


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


def normalize_other(image_ndarray, max_value=255, dtype=np.uint8) -> np.ndarray:
    image_ndarray = image_ndarray.astype(np.float64)
    max_var = np.max(image_ndarray != np.inf)
    image_ndarray = np.where(image_ndarray == np.inf, max_var, image_ndarray)
    temp_image = image_ndarray - np.min(image_ndarray)
    return ((temp_image) / ((np.max(temp_image)) * max_value)).astype(dtype)


def slice_image(image_ndarray: np.ndarray, indexes: list) -> np.ndarray:
    n_dim = len(image_ndarray.shape)
    slices = [slice(None)] * n_dim
    for i in range(len(indexes)):
        slices[i] = slice(indexes[i][0], indexes[i][1])
    slices = tuple(slices)
    sliced_image = image_ndarray[slices]
    return sliced_image


def mask_image_func(image_ndarray, mask_template_ndarray) -> np.ndarray:
    mask_ndarray = mask_template_ndarray
    return np.where(mask_ndarray == 255, image_ndarray, np.zeros(image_ndarray.shape))


def resize_image(patch_size, image):
    # only donwsampling, so use nearest neighbor that is faster to run
    resized_image = np.zeros(patch_size)
    for i in range(image.shape[0]):
        resized_image[i] = tf.image.resize(
            image[i], (patch_size[1], patch_size[2]
                       ), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR
        )
    # resized_image = tf.cast(resized_image, tf.float16)  # / 127.5 - 1.0
    return resized_image


def augment_image(image_ndarray):
    image = np.rot90(image_ndarray, axes=(2, 3), k=np.random.random_integers(0, 3))
    return image


def dilate_image(image):
    for h in range(image.shape[1]):
        image[0, h, :, :] = cv2.dilate(image[0, h, :, :].astype(np.uint8), self.dilate_kernel)
    return image


# Transformations
class Transpose:
    def __init__(self):
        pass

    def __call__(self, image):
        image = image.transpose(0, 4, 1, 2,
                                3)  # PyTorch expects the input tensor format for CNNs as (batch_size, channels, height, width).
        return image


train_transforms = transforms.Compose([
    # transforms.RandomHorizontalFlip(), # Flip the image horizontally
    # transforms.RandomRotation(degrees=10), # Rotate the image by up to 10 degrees
    # Transpose(),
    transforms.ToTensor(),  # Convert to a tensor
    transforms.Normalize((0.5,), (0.5,))  # Normalize values
])

test_transforms = transforms.Compose([
    # Transpose(),
    transforms.ToTensor(),  # Convert to a tensor
    transforms.Normalize((0.5,), (0.5,))  # Normalize values
])


class RegressionTestDataset(Dataset):
        """
        This class inherits from pytorch Dataset and defines basic functions that are
        needed for using pycharm operations on our data.
        """
        def __init__(self, csv_path, indices, transform=None, min_=0.0, max_=1.0):
            self.df = pd.read_csv(csv_path) # CSV with image locations
            self.indices = indices
            self.transform = transform # list of transformations on the data
            self.min_ = min_
            self.max_ = max_
            self.patches_from_image = 54 # Patches from test image

        def __len__(self):
            # Total patches for selected images
            num_selected_images = math.ceil((self.max_ - self.min_) * len(self.df))
            return num_selected_images * self.patches_from_image

        def __getitem__(self, index):
            if index >= len(self):
                raise IndexError("Index out of range")

            # Calculate which image and patch to access directly
            num_selected_images = math.ceil((self.max_ - self.min_) * len(self.df))
            start_idx = math.floor(len(self.df) * self.min_)

            # Compute image index and patch index from the given dataset index
            image_idx = start_idx + (index // self.patches_from_image) % num_selected_images
            patch_idx = index % self.patches_from_image

            # Load the correct image
            path = self.df.loc[image_idx, 'path_tiff']
            path = path.replace('Interpretability/interpretability', "")
            path = BASE_PATH + '/' + path.split('//')[1]
            image = np.array(tiff.imread(path))
            input_image = image[input_channel, :, :, :]
            target_image = image[target_channel, :, :, :]

            # Apply normalization
            input_image = normalize_std(input_image)

            # Access the specific patch
            sx, sy = self.indices[patch_idx]  # Directly map to the correct indices
            input_patch, target_patch = get_patch(input_image, target_image, sx, sy)

            input_patch = np.expand_dims(input_patch, axis=-1)
            input_patch = np.expand_dims(input_patch, axis=0)
            target_patch = np.expand_dims(target_patch, axis=-1)
            target_patch = np.expand_dims(target_patch, axis=0)

            target_prediction = unet(input_patch)
            mask_prediction = mg.generator([input_patch, target_prediction]) # Check if casting is needed
            error_rate = 1 - abs(tf_pearson_corr(target_prediction, tf.cast(target_patch, tf.float64)))
            error_rate = tf.where(tf.math.is_nan(error_rate), tf.zeros_like(error_rate), error_rate)

            mask_prediction = mask_prediction.numpy()
            combined_input = np.concatenate([target_prediction, mask_prediction], axis=-1)

            combined_input = torch.from_numpy(combined_input).float()
            combined_input = combined_input.permute(0, 4, 1, 2, 3)
            combined_input = combined_input.squeeze(0)
            error_rate = torch.tensor([error_rate.numpy()], dtype=torch.float32)

            return combined_input, error_rate, input_patch, target_patch


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
organelles = ["Mitochondria", "Nucleolus-(Granular-Component)", "Nuclear-envelope", "Actin-filaments", "Microtubules",
              "Plasma-membrane", "Endoplasmic-reticulum", "DNA"]

save_folder = f"{BASE_PATH}/variables"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)
    
for organelle in organelles:
    unet_model_path = f"{BASE_PATH}/models/unet/{organelle}/"
    mg_model_path = f"{BASE_PATH}/models/mg/{organelle}/"
    conf_model_path = f"{BASE_PATH}/models/confidence/{organelle}/conf_model.pt"
    test_csv_path = f"{BASE_PATH}/data/{organelle}/image_list_test.csv"

    input_channel=0
    if organelle == "DNA":
        target_channel = 1
    else:
        target_channel = 3

    # Load neccessary models
    unet = keras.models.load_model(unet_model_path)
    mg = keras.models.load_model(mg_model_path)
    conf_model = ResNet3DRegression(fine_tune_layers='partial')
    conf_model.load_state_dict(torch.load(conf_model_path, weights_only=True))
    conf_model.eval()

    indices = {}
    i = 0
    for x in range(0, 496, 96):
        for y in range(0, 796, 96):
            indices[i] = (x,y)
            i += 1

    # Check use of GPU
    if torch.cuda.is_available():
        print("GPU is available")
        device = torch.device("cuda")
    else:
        print("GPU is not available")
        device = torch.device("cpu")  # Fallback to CPU if GPU is not available

    # Load data
    test_data = RegressionTestDataset(test_csv_path, transform=test_transforms, indices=indices)

    # Data size
    print(f"Test data length in patches: {len(test_data)}")

    # Run Test

    error_predictions = []
    errors = []

    for i in range(len(test_data)):
        img, err, ip, tp = test_data[i]
        errors.append(err.numpy()[0])
        img = torch.from_numpy(np.expand_dims(img, axis=0)).float()
        pred = conf_model(img)
        error_predictions.append(float(pred))

    # Save errors+error_predictions
    error_predictions_np = np.array(error_predictions)
    np.save(f"{BASE_PATH}/variables/{organelle}_Error_Predictions.npy", error_predictions_np)
    errors_np = np.array(errors)
    np.save(f"{BASE_PATH}/variables/{organelle}_Errors.npy", errors_np)
