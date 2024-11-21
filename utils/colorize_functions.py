# -*- coding:utf-8 -*-
import sys
sys.path.append('/home/zoe/ResearchProjects/DesignGenerationVector')
import cv2
from random import randint as ri
from random import uniform as rf
import numpy as np 
import math
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

from collections import Counter
from setting import savePath, imgPath, elementPath, processPath, keepPath, svgPath, colorrefPath

import warnings
warnings.filterwarnings("ignore")


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(rgb):
    hex_code = '#'
    for i in rgb:
        if np.isnan(i):
            i = 255
        else:
            num = int(i)
            # hex += str(hex(num))[-2:].replace('x', '0').upper()
        hex_code += f'{num:02X}'
    return hex_code


def hex_random():
    # generate a random hes code
    color1 = ri(0, 255)
    color2 = ri(0, 255)
    color3 = ri(0, 255)
    color1 = hex(color1)
    color2 = hex(color2)
    color3 = hex(color3)
    ans = "#" + color1[2:] + color2[2:] + color3[2:]
    return ans


def calculate_color_distance(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2

    r_mean = (r1 + r2) / 2
    r_diff = r1 - r2
    g_diff = g1 - g2
    b_diff = b1 - b2

    return math.sqrt(
        (2 + r_mean / 256) * (r_diff ** 2) +
        4 * (g_diff ** 2) +
        (2 + (255 - r_mean) / 256) * (b_diff ** 2)
    )



def colorize_histogram(img, name, visualization):
    img = img.reshape((-1, 1))

    # # color histogram v2
    hist = cv2.calcHist([img], [0], None, [26], [0.0, 256.0])
    minVal_b, maxVal_b, minLoc_b, maxLoc_b = cv2.minMaxLoc(hist)
    A = np.sum(hist)
    hist_ = hist / A
    B = hist_.flatten().tolist()

    if visualization:
        plt.bar(range(len(B)), B)
        plt.title('Grayscale Histogram')
        plt.xlabel('Bins')
        plt.ylabel('# of Pixels')
        plt.savefig(processPath + name + '_' + "gray_color_dis_hist.png")
        # plt.show()
        plt.close('all')

    num = []
    for item in B:
        if item > 0.02:
            num.append(item)

    if len(num) > 1:
        return len(num)
    else:
        return 2
    

def show_color_blocks(cluster_rgb, name):
    width = 2.8
    height = 4
    block_height = 0.4  # Fixed block height
    block_width = 1.5  # Fixed block width
    font_size = 8  # Fixed font size for clarity

    color_fig = plt.figure(figsize=(width, height))
    box = color_fig.add_subplot(111)

    for i, color in enumerate(cluster_rgb):
        face_color = tuple(np.array(color) / 255)
        loc_y = -i * block_height - 0.5
        tmp_box = plt.Rectangle((-0.3, loc_y), block_width, block_height, facecolor=face_color, edgecolor='gray', linewidth=0.1, fill=True)
        box.add_patch(tmp_box)
        plt.text(1.25, loc_y + block_height / 2, f"[{color[0]}, {color[1]}, {color[2]}]", fontsize=font_size, va='center', ha='left')

    plt.xlim(-0.5, 2)
    plt.ylim(-height - 0.5, 0)  
    plt.axis('off')
    color_fig.savefig(name, bbox_inches='tight', pad_inches=0.1)
    plt.close(color_fig)
    

def generate_color_palette(im, k):
    # k-means for color reduction
    temp_im = cv2.cvtColor(im, cv2.COLOR_BGR2LAB)  # convert to LAB
    temp_im = temp_im.reshape((-1, 3))
    k_colors = KMeans(n_clusters=k)
    k_colors.fit(temp_im)
    labels = k_colors.predict(temp_im)
    cluster_colors = k_colors.cluster_centers_

    img0 = np.ones((2, 2), dtype=np.uint8)
    rgb_img = cv2.cvtColor(img0, cv2.COLOR_GRAY2RGB)  # convert to rgb
    cluster_rgb = []
    for i in cluster_colors:
        h, s, v = (i[0], i[1], i[2])
        rgb_img[:, :, :] = (h, s, v)
        RGB = cv2.cvtColor(rgb_img, cv2.COLOR_LAB2RGB)  # or cv2.COLOR_HSV2RGB)
        cluster_rgb.append(RGB[1, 1, :].tolist())

        # Count occurrences of each label
    label_counts = Counter(labels)

    # Sort clusters by the number of pixels assigned to them
    sorted_indices = [label for label, count in label_counts.most_common()]

    # Sort cluster_rgb based on sorted_indices
    sorted_cluster_rgb = [cluster_rgb[i] for i in sorted_indices]

    return cluster_rgb, sorted_cluster_rgb, labels
