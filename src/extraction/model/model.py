import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable
import torch.nn.init
import random
import math

import cv2
# print(cv2.__version__)
import imutils
from scipy import stats
from matplotlib import pyplot as plt
import sys
import os
import numpy as np
from skimage import segmentation
from skimage.segmentation import mark_boundaries
from skimage.feature import peak_local_max
from scipy import ndimage as ndi

use_cuda = torch.cuda.is_available()


class MyNet(nn.Module):
    """CNN model"""
    def __init__(self, input_dim):
        super(MyNet, self).__init__()
        self.conv1 = nn.Conv2d(input_dim, 100, kernel_size=3, stride=1, padding=1 )
        self.bn1 = nn.BatchNorm2d(100)
        self.conv2 = nn.ModuleList()
        self.bn2 = nn.ModuleList()

        for i in range(2-1):
            self.conv2.append( nn.Conv2d(100, 100, kernel_size=3, stride=1, padding=1 ) )
            self.bn2.append( nn.BatchNorm2d(100) )

        self.conv3 = nn.Conv2d(100, 100, kernel_size=1, stride=1, padding=0 )
        self.bn3 = nn.BatchNorm2d(100)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu( x )
        x = self.bn1(x)
        for i in range(2-1):
            x = self.conv2[i](x)
            x = F.relu( x )
            x = self.bn2[i](x)
        x = self.conv3(x)
        x = self.bn3(x)
        return x

