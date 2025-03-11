# -*- coding:utf-8 -*-
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
from .model import MyNet

from setting import savePath, imgPath, elementPath, processPath

use_cuda = torch.cuda.is_available()


def segment_img(img, maxIter, name, visualization):
    data = torch.from_numpy(np.array([img.transpose((2, 0, 1)).astype('float32')/255.]))
    if use_cuda:
        data = data.cuda()
    data = Variable(data)

    seg_map = segmentation.felzenszwalb(img, scale=2, sigma=0.5, min_size=2048)
    if visualization:
        cv2.imwrite(processPath + name + '_out_' + 'felzenszwalb' + '.png', seg_map)

    seg_map = seg_map.flatten()
    l_inds = [np.where(seg_map == u_label)[0] for u_label in np.unique(seg_map)]

    model = MyNet(data.size(1))

    if use_cuda:
        model.cuda()

    model.train()
    loss_fn = torch.nn.CrossEntropyLoss()
    # optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.9)
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    label_colours = np.random.randint(200, size=(100, 3))  # random 200 color_rgb

    Loss_record = []
    min_delta = 0.01
    record_counter = 0
    for batch_idx in range(maxIter):
        # forwarding
        optimizer.zero_grad()
        output = model(data)[0]
        output = output.permute(1, 2, 0).contiguous().view(-1, 100)
        ignore, target = torch.max(output, 1)
        im_target = target.data.cpu().numpy()
        nLabels = len(np.unique(im_target))

        # refinement
        for i in range(len(l_inds)):
            labels_per_sp = im_target[l_inds[i]]
            u_labels_per_sp = np.unique(labels_per_sp)
            hist = np.zeros(len(u_labels_per_sp))
            for j in range(len(hist)):
                hist[j] = len(np.where(labels_per_sp == u_labels_per_sp[j])[0])
            im_target[l_inds[i]] = u_labels_per_sp[np.argmax(hist)]

        # backward
        target = torch.from_numpy(im_target)
        if use_cuda:
            target = target.cuda()
        target = Variable(target)

        loss = loss_fn(output, target)

        # loss_np = loss.data.cpu().numpy()
        # np.save(processPath + '/epoch_{}'.format(batch_idx), loss_np)

        Loss_record.append(loss)
        loss.backward()
        optimizer.step()

        if nLabels <= 3 or record_counter >= 3:
            break

        if batch_idx > 0:
            delt = Loss_record[batch_idx - 1] - Loss_record[batch_idx]
            if delt < min_delta:
                record_counter += 1

        output = model(data)[0]
        output = output.permute(1, 2, 0).contiguous().view(-1, 100)
        ignore, target = torch.max(output, 1)
        im_target = target.data.cpu().numpy()

        # save output for visulization
        im_target_rgb = np.zeros((im_target.shape[0], 3))
        for c in range(im_target.shape[0]):
            im_target_rgb[c] = np.array(label_colours[im_target[c] % 100])
        im_target_rgb = im_target_rgb.reshape(img.shape).astype(np.uint8)
        cv2.imwrite(processPath + name + '_unspervised_segment.png', im_target_rgb)

    return im_target


