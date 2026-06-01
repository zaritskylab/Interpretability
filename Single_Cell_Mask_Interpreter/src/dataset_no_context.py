import os
import numpy as np
import pandas as pd
import tifffile
import torch
import inspect
from torch.utils.data import Dataset


class DataGen(Dataset):
    def __init__(self, csv_path, image_dir, transforms=None, signals_are_masked=False):
        self.df = pd.read_csv(csv_path)
        self.image_dir = image_dir
        self.transforms = transforms or {'signal': [], 'target': [], 'mask': []}
        self.signals_are_masked = signals_are_masked

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        signal = tifffile.imread(os.path.join(self.image_dir, row["signal_file"])).astype(np.float32)
        target = tifffile.imread(os.path.join(self.image_dir, row["target_file"])).astype(np.float32)

        # Load mask if applicable
        mask = None
        if self.signals_are_masked:
            mask = tifffile.imread(os.path.join(self.image_dir, row["mask_file"])).astype(np.float32)

        # Apply transforms
        for t in self.transforms['signal']:
            if mask is not None and 'mask' in inspect.signature(t).parameters:
                signal = t(signal, mask)
            else:
                signal = t(signal)
        
        for t in self.transforms['target']:
            if mask is not None and 'mask' in inspect.signature(t).parameters:
                target = t(target, mask)
            else:
                target = t(target)
        
        if mask is not None:
            for t in self.transforms['mask']:
                mask = t(mask)

        # Convert to torch tensors, shape: (C, D, H, W)
        signal = torch.tensor(signal[np.newaxis, ...])
        target = torch.tensor(target[np.newaxis, ...])

        return signal, target, mask