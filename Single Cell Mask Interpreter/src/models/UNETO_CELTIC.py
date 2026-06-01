import torch
import torch.nn as nn
import torch.nn.functional as F


# Check this function
def center_crop(tensor, target_tensor):
    _, _, d, h, w = target_tensor.shape
    d1, h1, w1 = tensor.shape[2:]
    d_start = (d1 - d) // 2
    h_start = (h1 - h) // 2
    w_start = (w1 - w) // 2
    return tensor[:, :, d_start:d_start+d, h_start:h_start+h, w_start:w_start+w]


class DoubleConv(nn.Module):
    def __init__(self, in_channels, out_channels, batch_norm=True):
        super(DoubleConv, self).__init__()
        layers = [
            nn.Conv3d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.Conv3d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
        ]
        if batch_norm:
            layers.insert(1, nn.BatchNorm3d(out_channels))
            layers.insert(-1, nn.BatchNorm3d(out_channels))
        self.double_conv = nn.Sequential(*layers)

    def forward(self, x):
        return self.double_conv(x)


class Down(nn.Module):
    def __init__(self, in_channels, out_channels, batch_norm=True):
        super(Down, self).__init__()
        self.maxpool_conv = nn.Sequential(
            nn.Conv3d(in_channels, out_channels, kernel_size=4, stride=2, padding=1),
            nn.ReLU(inplace=True),
            DoubleConv(out_channels, out_channels, batch_norm=batch_norm)
        )

    def forward(self, x):
        return self.maxpool_conv(x)


class Up(nn.Module):
    def __init__(self, in_channels, out_channels, batch_norm=True):
        super(Up, self).__init__()
        self.up = nn.ConvTranspose3d(in_channels, out_channels, kernel_size=4, stride=2, padding=1)
        self.conv = DoubleConv(in_channels, out_channels, batch_norm=batch_norm)

    # Check this function
    def forward(self, x1, x2):
        x1 = self.up(x1)
        x = torch.cat([x2, x1], dim=1)
        return self.conv(x)


class UpBottleneck(nn.Module):
    def __init__(self, in_channels, out_channels, batch_norm=True):
        super(UpBottleneck, self).__init__()
        self.up = nn.ConvTranspose3d(in_channels, out_channels, kernel_size=4, stride=2, padding=1)
        self.conv = DoubleConv(in_channels, out_channels, batch_norm=batch_norm)

    # Check this function
    def forward(self, x1, x2):
        x = torch.cat([x2, x1], dim=1)
        return self.conv(x)


class OutConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(OutConv, self).__init__()
        self.conv = nn.Conv3d(in_channels, out_channels, kernel_size=3, padding=1)

    def forward(self, x):
        return self.conv(x)


class UNet3D(nn.Module):
    def __init__(self, in_channels=1, out_channels=1, base_filters=16, batch_norm=True):
        super(UNet3D, self).__init__()
        self.inc = DoubleConv(in_channels, base_filters, batch_norm=batch_norm)
        self.down1 = Down(base_filters, base_filters * 2, batch_norm=batch_norm)
        self.down2 = Down(base_filters * 2, base_filters * 4, batch_norm=batch_norm)
        self.down3 = Down(base_filters * 4, base_filters * 8, batch_norm=batch_norm)
        self.bottleneck = DoubleConv(base_filters * 8, base_filters * 16, batch_norm=batch_norm)
        self.reduce_channels = nn.Conv3d(in_channels=256, out_channels=128, kernel_size=1)
        self.up1 = UpBottleneck(base_filters * 16, base_filters * 8, batch_norm=batch_norm)
        self.up2 = Up(base_filters * 8, base_filters * 4, batch_norm=batch_norm)
        self.up3 = Up(base_filters * 4, base_filters * 2, batch_norm=batch_norm)
        self.up4 = Up(base_filters * 2, base_filters, batch_norm=batch_norm)
        self.outc = OutConv(base_filters, out_channels)

    def forward(self, x):
        x1 = self.inc(x)
        x2 = self.down1(x1)
        x3 = self.down2(x2)
        x4 = self.down3(x3)
        x5 = self.bottleneck(x4)
        x5_reduced = self.reduce_channels(x5)
        x = self.up1(x5_reduced, x4)
        x = self.up2(x, x3)
        x = self.up3(x, x2)
        x = self.up4(x, x1)
        logits = self.outc(x)
        return torch.sigmoid(logits)