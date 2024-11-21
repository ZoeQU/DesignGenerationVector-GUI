# -*- coding:utf-8 -*-
import sys
sys.path.append('/home/zoe/ResearchProjects/DesignGenerationVector')
import setting
import numpy as np
import os
import cv2
import imutils
import pandas as pd
import json
import math
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
from skimage.metrics import structural_similarity as ssim

from setting import savePath, imgPath, elementPath, processPath, keepPath, svgPath, colorrefPath

from .model.segment_img import segment_img
from utils.image_processing import resize_img



def find_background_mask(img, name, processPath, maxIter, visualization):
    im_target = segment_img(img, maxIter, name, False)

    masks = []
    colors = np.unique(im_target)
    num_color = len(colors)
    for k in range(num_color):
        color = colors[k]
        im_target_ = im_target.copy()
        im_target_ = np.where(im_target_ == color, 255, 0)  # white|255:content black|0:background
        im_target2_ = np.where(im_target == color, 1, 0)  # save color mask [0,1]

        im_target_ = im_target_.reshape((img.shape[0], img.shape[1])).astype(np.uint8)
        masks.append(im_target_)

        if visualization: #save rgb bk mask
            im_target2_ = im_target2_.reshape((img.shape[0], img.shape[1])).astype(np.uint8)
            b, g, r = cv2.split(img)
            im_target2_ = cv2.merge([im_target2_ * b, im_target2_ * g, im_target2_ * r])
            cv2.imwrite(processPath + name + '_out_' + str(k) + '.png', im_target2_)  # save each color mask


    # which one is the background mask
    bk_mask = find_bk_by_cut_coord(masks)  #TODO (3 nov): double check the shape of each mask
    return bk_mask

def find_bk_by_cut_coord(masks):
    bk_candidates = []
    num_bk_pixel = []
    for mask in masks:
        flatten_mask = mask.flatten()
        num_bk_pixel.append(np.count_nonzero(flatten_mask))

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # cnts = contours[0] if imutils.is_cv2() else contours[1]
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)  # bounding box
            if mask.shape[1] - w < 10 and mask.shape[0] - h < 10:
                bk_candidates.append(mask)
                break

    if len(bk_candidates) == 0:
        bk_mask = masks[np.argmax(np.array(num_bk_pixel))]
    elif len(bk_candidates) > 1:
        axis_2 = np.count_nonzero(np.array(bk_candidates), axis=2)
        s2 = np.sum(axis_2, axis=1)
        bk_mask = bk_candidates[np.argmax(s2)]
    else:
        bk_mask = bk_candidates[0]
    return bk_mask
        
def extract_background_color(img, name, visualization, maxIter=50):
    scale = 100 # resize scale
    if scale != 100:
        img = resize_img(img, scale)

    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
    dim = (1, 3, img.shape[1], img.shape[0])

    # temp_bk = []
    bk_mask = find_background_mask(img, name, processPath, maxIter, visualization)
    temp_bk = bk_mask.squeeze()
    # temp_bk.append(bk_mask)
    # temp_bk.append(bk_mask)  # 就写两次 不能删

    if visualization:   # bk masks visualization
        plt.imshow(temp_bk, 'gray')
        # plt.axis('off')
        plt.savefig(processPath + name + "_bk_mask" + ".png")
        # plt.show()
        plt.close('all')
    return bk_mask

def find_minimum_bounding_box(box):
    box_ = box[0].tolist()
    aa = sorted(box_, key=lambda x: x[0])
    minx = aa[0][0]
    maxx = aa[-1][0]
    bb = sorted(box_, key=lambda x: x[1])
    miny = bb[0][1]
    maxy = bb[-1][1]
    return [minx, miny, maxx, maxy]

def anomaly_cut(image, box, min_box, k, bk_color, name):
    # Create an image with the background color
    rows = image.shape[0]
    cols = image.shape[1]
    channels = image.shape[2]
    image2 = np.zeros(image.shape, dtype=np.uint8)
    image2[:, :, 0] = np.ones([rows, cols]) * bk_color[2]  # B
    image2[:, :, 1] = np.ones([rows, cols]) * bk_color[1]  # G
    image2[:, :, 2] = np.ones([rows, cols]) * bk_color[0]  # R

    # Create a mask for irregular polygon cutting
    mask_cut = np.zeros(image.shape, dtype=np.uint8)
    roi_corners = box
    cv2.fillPoly(mask_cut, roi_corners, (255, 255, 255))  # White element on black mask

    # Apply mask to create the cut-out
    aa = mask_cut[:, :, 0]
    aa = np.where(aa == 255, 0, 1)
    bb = image2[:, :, 0] * aa
    gg = image2[:, :, 1] * aa
    rr = image2[:, :, 2] * aa
    mask_cut2 = cv2.merge([bb, gg, rr])  # mask_cut: bk_color mask, 黑element

    # Bitwise AND to extract the masked image
    masked_image = cv2.bitwise_and(image, mask_cut)

    b, g, r = cv2.split(masked_image)
    masked_image2 = cv2.merge([bb + b, gg + g, rr + r])

    # region
    # plt.subplot(141)
    # plt.imshow(mask_cut)
    # plt.subplot(142)
    # plt.imshow(mask_cut2)
    # plt.subplot(143)
    # plt.imshow(masked_image)
    # plt.subplot(144)
    # plt.imshow(masked_image2)
    # plt.show()
    # plt.close()
    # endregion

    # Save elements and masked image
    delements = masked_image2[min_box[1]: min_box[3], min_box[0]: min_box[2]]
    cv2.imwrite(elementPath + name + '_' + str(k) + '_cc_element.png', delements)
    cv2.imwrite(processPath + name + '_' + str(k) + '_cc_masked.png', masked_image2)
    return masked_image2, delements

def irregular_cut(img, bk_mask, bk_color, name, visulization):
    kernel = np.ones((3, 3), dtype=np.uint8)
    bk_mask = cv2.morphologyEx(bk_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    contours, _ = cv2.findContours(bk_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    if visulization:
        contour_image = cv2.cvtColor(bk_mask, cv2.COLOR_GRAY2BGR)
        cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
        cv2.imwrite(processPath + name + "_contours.png", contour_image)

    bottom = np.zeros(img.shape, np.uint8) # create a mask
    bottom.fill(255)
    top = img.copy()
    # overlapping = cv2.addWeighted(bottom, 0.7, top, 0.3, 0)

    de_object_bboxes = []
    de_segments = []
    cuttingImgs = []
    for k in range(len(contours)):
        try:
            cont = contours[k]
            if cont.shape[0] > 3:
                epsilon = 0.002 * cv2.arcLength(cont, True)
                box = cv2.approxPolyDP(cont, epsilon, True)
                M = cv2.moments(cont) 
                centerx = int(M["m10"] / (M["m00"] + 0.01))
                centery = int(M["m01"] / (M["m00"] + 0.01))
                new_box = []
                for i in box:
                    vx = 1.1 * (centerx - i[0][0])
                    vy = 1.1 * (centery - i[0][1])
                    nx = int(math.ceil(centerx - vx))
                    if nx < 0 or nx > img.shape[1]:
                        nx = i[0][0]
                    ny = int(math.ceil(centery - vy))
                    if ny < 0 or ny > img.shape[0]:
                        ny = i[0][1]
                    new_box.append([[nx, ny]])

                new_box = np.array(new_box)
                new_box_reshape = np.reshape(new_box, (1, -1, 2))
   
                # calculate the area
                mask_area = np.zeros(img.shape[:2], dtype="uint8")
                polygon_mask = cv2.fillPoly(mask_area, new_box_reshape, 255)
                area = np.sum(np.greater(polygon_mask, 0))  # after scale 1.1 times
                area_ori = cv2.contourArea(cont)  # ori_area
                if area_ori > 300 and area_ori < 0.5 * img.shape[0] * img.shape[1]:  # thre=100
                    min_box = find_minimum_bounding_box(new_box_reshape)  # find bbox
                    de_segments.append(new_box)
                    de_object_bboxes.append(min_box)
                    if min_box[3] - min_box[1] > 0.067 * img.shape[1] and min_box[2] - min_box[0] > 0.067 * img.shape[0]:
                        masked_image, delements = anomaly_cut(img, new_box_reshape, min_box, k, bk_color, name)
                        cuttingImg = [area, masked_image, delements]
                        cuttingImgs.append(cuttingImg)

                        if visulization:
                            pts_oribox = box.reshape((-1, 1, 2))
                            img = cv2.polylines(img, pts=[pts_oribox], isClosed=True, color=(31, 23, 176), thickness=1)  # green
                            img = cv2.polylines(img, pts=[new_box_reshape], isClosed=True, color=(103, 54, 16), thickness=2)  # blue
                            cv2.imwrite(processPath + name + '_' + str(k) + '_temp_irregular_cut.png', img)

        except Exception as e:
            de_segments = None
            de_object_bboxes = None
            cuttingImgs = None
            continue

    if cuttingImgs is None or len(cuttingImgs) > (img.shape[0] / 30 * img.shape[1] / 30):
        return None, None, None
    else:
        return cuttingImgs, de_object_bboxes, de_segments


def compare_images(imageA, imageB):
    imageA = imageA.astype('uint8')
    imageB = imageB.astype('uint8')
    # Resize images to a common size
    common_size = (200, 200)
    imageA_resized = cv2.resize(imageA, common_size)
    imageB_resized = cv2.resize(imageB, common_size)
    
    # Convert to grayscale
    grayA = cv2.cvtColor(imageA_resized, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB_resized, cv2.COLOR_BGR2GRAY)
    
    # Compute SSIM
    score, _ = ssim(grayA, grayB, full=True)
    return score
