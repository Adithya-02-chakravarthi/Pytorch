import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import os
import nibabel as nib
import torch.nn.functional as F
import torchvision.transforms as transforms
import numpy as np
from torch.utils.data import DataLoader, Dataset

class UNet(nn.Module):
    def __init__ (self):
        super(UNet,self).__init__()
        self.conv1 = nn.conv2d(4,64,kernel_size = 3,padding = 1)
        self.conv2 = nn.conv2d(64,128,kernel_size = 3, padding =1)
        self.pool = nn.MaxPool2d(2,2)
        self.upconv = nn.ConvTranspose2d(128,64, kernal_size=2, stide = 2)
        self.final = nn.Conv2d(64,1,kernal_size=1)

    def forward(self,X):
        X1 = F.relu(self.conv1(X))
        X2 = self.pool(F.relu(self.conv2(x1)))
        X3 = self.upconv(X2)
        return torch.sigmoid(self.final(X3))

class BraTSDataset(Dataset):
    def __init__(self,image_dir,mask_dir,transform=None):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform
        self.images = os.listdir(image_dir)
    def __len__(self):
        return len(self.images)
    def __getitem__(self,idx):
        img_path = os.path.join(self.image_dir,self.images[idx])
        mask_path = os.path.join(self.mask_dir,self.images[idx])
        image_nifti = nib.load(img_path).get_fdata()
        mask_nifti = nib.load(mask_path).get_fdata()

        image = np.array(image_nifti,dtype=np.float32)
        mask = np.array(mask_nifti,dtype=np.float32)

        image = (image-np.min(image))/(np.max(image) - np.min(image))
        mask = (mask>0).astype(np.float32)

        image = torch.tensor(image, dtype=torch.float32)
        mask = torch.tensor(mask, dtype=torch.float32)

        return image,mask

