# -*- coding:utf-8 -*-
import sys
sys.path.append('/home/zoe/ResearchProjects/DesignGenerationVector')
import numpy as np
import itertools
import os
import time
import cv2
from skimage.metrics import structural_similarity as ssim
import imutils
from setting import savePath, imgPath, elementPath, processPath, keepPath, svgPath, colorrefPath
import random
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt

from utils.image_processing import resize_img
from .extract_functions import extract_background_color, irregular_cut, compare_images
# from perceptualhashing import cal_perceptual_hashing_similarity
from utils.figure_ploter import visualize_pie_chart, visualize_hist


import warnings
warnings.filterwarnings("ignore")


def extract_foreground_elements(img, name, thre, visualization):
    scale = 100 # resize scale
    if scale != 100:
        img = resize_img(img, scale)

    bk_mask = extract_background_color(img, name, visualization, maxIter=50)
    B, G, R = cv2.split(img)
    # region
    # bk_01 = np.where(bk_mask == 255, 1, 0)  # binary
    # B_ = int(B[np.nonzero(bk_01 * B)].mean())
    # G_ = int(G[np.nonzero(bk_01 * G)].mean())
    # R_ = int(R[np.nonzero(bk_01 * R)].mean())
    # bk_color = [R_, G_, B_]  # rbg value
    # rr = bk_01 * R_
    # gg = bk_01 * G_
    # bb = bk_01 * B_
    # im_bk_rgb = cv2.merge([bb, gg, rr])
    # endregion
    bk_01 = (bk_mask == 255).astype(np.uint8)
    B_ = int(np.mean(B[bk_01 != 0]))
    G_ = int(np.mean(G[bk_01 != 0]))
    R_ = int(np.mean(R[bk_01 != 0]))
    bk_color = [R_, G_, B_]  # RGB values
    im_bk_rgb = cv2.merge([bk_01 * B_, bk_01 * G_, bk_01 * R_])

    if visualization:  # bk_color rgb mask
        cv2.imwrite(processPath + name + '_bk_mask_rgb.png', im_bk_rgb)

    # irregular cutting 
    cuttingImgs, de_object_bboxes, de_segments = irregular_cut(img, bk_mask, bk_color, name, visualization)

    if cuttingImgs == None:
        cuttingImgs = img

    if de_object_bboxes == None:
        h = img.shape[0]
        w = img.shape[1]
        de_object_bboxes = [0, 0, w, h]
        de_segments = [[0, 0], [w, 0], [w, h], [0, h]]

    print('crop element: ' + str(len(cuttingImgs)))
    return bk_color, cuttingImgs, bk_mask, de_segments, de_object_bboxes, thre


def remove_redundant_elements(name, cuttingImgs, thre, visualization):
    Group = cuttingImgs 

    if len(Group) == 1:
        keep = Group[0][2]
        name = keepPath + name + '_' + str(0) + '.png'
        cv2.imwrite(name, Group[0][2])
        print('keep elements: %s' % len(Group))
        return Group, keep
   
    else:   # Similarity comparison
        GG = list(itertools.combinations(Group, 2))
        # sim = []
        # for gg in GG:
        #     # contentMatchRatio = cal_perceptual_hashing_similarity(gg[0][2].astype('uint8'), gg[1][2].astype('uint8'))
        #     # similarity = np.mean(contentMatchRatio[:-2])
        #     # sim.append(similarity)
        #     contentMatchRatio = compare_images(gg[0][2].astype('uint8'), gg[1][2].astype('uint8'))
        #     sim.append(contentMatchRatio)
        #     # print(contentMatchRatio)
        # 
        # if visualization:
        #     visualize_pie_chart(sim, processPath, "Perceptual Hashing")

        # thre = 0.1 # simlar threshod

        Group_copy = Group.copy() 
        keep = []
        while len(Group_copy) > 0:
            Group_copy = sorted(Group_copy, key=lambda x: x[0])  # area从小到大排序
            t = Group_copy[-1]
            keep.append(Group_copy[-1][2])
            Group_copy = Group_copy[:-1]

            del_list = []
            for i in range(len(Group_copy)):
                # contentMatchRatio = cal_perceptual_hashing_similarity(Group_copy[i][2], t[2])
                # similarity = np.mean(contentMatchRatio[:-2])
                contentMatchRatio = compare_images(Group_copy[i][2], t[2])
                # print(contentMatchRatio)
                similarity = contentMatchRatio
                print(similarity)
                if similarity > thre:
                    del_list.append(Group_copy[i])

            if len(del_list) > 0:
                for k in range(len(del_list)):
                    try:
                        Group_copy.remove(del_list[k])
                    except Exception as e:
                        continue

        if len(keep) > 0:
            for q in range(len(keep)):
                name_ = keepPath + name + '_' + str(q) + '.png'
                cv2.imwrite(name_, keep[q])
            print('keep elements: %s' % len(keep))
        else:
            name = keepPath + name + '_' + str(0) + '.png'
            img = cv2.imread(imgPath + name)
            cv2.imwrite(name, img)
            print('keep elements: %s' % 1)
        return Group, keep
    

def extractor(img, name, thre, visualization):
    bk_color, cuttingImgs, bk_mask, de_segments, de_object_bboxes, thre = extract_foreground_elements(img, name, thre, visualization)
    Group, keep = remove_redundant_elements(name, cuttingImgs, thre, visualization)
    # print(len(Group), len(keep), bk_color)
    return bk_color, keep


if __name__ == "__main__":
    image_path = imgPath + "test.jpg"
    name = image_path.split("/")[-1].split(".")[0]
    print(name)
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    bk_color, keep = extractor(img, name + "_" + name, visualization=True)
    print("biu~ biu~ biu~")