import torch
import numpy as np
from math import log10, sqrt


def psnr(original, compressed):
    mse = torch.mean((original - compressed) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr_val = 20 * log10(max_pixel / sqrt(mse.item()))
    return psnr_val


def torch_pearson_corr_aux(x, y):
    mean_x = torch.mean(x)
    mean_y = torch.mean(y)
    std_x = torch.std(x - mean_x)
    std_y = torch.std(y - mean_y)
    cc = torch.mean((x - mean_x) * (y - mean_y)) / (std_x * std_y + 1e-8)
    return cc


def pearson_corr_torch(y_true, y_pred, weights=None):
    y_true_flat = y_true.view(-1)
    y_pred_flat = y_pred.view(-1)

    if weights is not None:
        weights_flat = weights.view(-1)
        ind = (weights_flat == 1.0) | (weights_flat == 255.0)
        non_ind = ~ind

        cc = 0.0
        t_weights = [1.0, 0.0]
        for i, mask in enumerate([ind, non_ind]):
            if mask.sum() > 0:
                x = y_true_flat[mask]
                y = y_pred_flat[mask]
                cc += t_weights[i] * torch_pearson_corr_aux(x, y)
            else:
                cc += t_weights[i]
    else:
        cc = torch_pearson_corr_aux(y_true_flat, y_pred_flat)

    return cc


def pearson_corr_numpy(a, b, weights=None):
    if weights is not None:
        ind = (weights == 1.0) | (weights == 255.0)
        non_ind = ~(ind)

        cc = 0
        t_weights = [1.0, 0.0]
        for i, mask in enumerate([ind, non_ind]):
            if np.sum(mask) > 0:
                x = a[mask]
                y = b[mask]
                cc += t_weights[i] * pearson_corr_aux_numpy(x, y)
            else:
                cc += t_weights[i]
    else:
        a_mask = a != 1e-4
        x = a[a_mask]
        y = b[a_mask]
        cc = pearson_corr_aux_numpy(x, y)

    return cc


def pearson_corr_aux_numpy(a, b):
    mean_a = np.mean(a)
    mean_b = np.mean(b)
    std_a = np.std(a - mean_a)
    std_b = np.std(b - mean_b)
    cc = np.mean((a - mean_a) * (b - mean_b)) / (std_a * std_b + 1e-8)
    return cc


def dice_score(a, b):
    # a and b should be binary masks (same shape, torch or numpy)
    if isinstance(a, torch.Tensor):
        a = a.cpu().numpy()
    if isinstance(b, torch.Tensor):
        b = b.cpu().numpy()

    intersection = np.sum(b[a == 1])
    return (2.0 * intersection) / (np.sum(b) + np.sum(a) + 1e-4)