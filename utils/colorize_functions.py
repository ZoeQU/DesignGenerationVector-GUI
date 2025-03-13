# -*- coding:utf-8 -*-
import sys
sys.path.append('/home/zoe/ResearchProjects/DesignGenerationVector')
import cv2
from random import randint as ri
from random import uniform as rf
import numpy as np 
import math
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
import re
import heapq
import pandas as pd 

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
    

def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range

def color3dshow(im, temp_folder, files):
    """show pixel in 3d"""
    im = np.array(im)
    im2 = im.reshape((-1, 3))
    fig = plt.figure()
    ax = Axes3D(fig)
    for i in im2:
        c = i * 1.2 / 255
        c = normalization(c)
        ax.scatter(i[0], i[1], i[2], c=c, label='顺序点')
    ax.set_zlabel('B', fontdict={'size': 15, 'color': 'red'})
    ax.set_ylabel('G', fontdict={'size': 15, 'color': 'red'})
    ax.set_xlabel('R', fontdict={'size': 15, 'color': 'red'})
    plt.savefig(temp_folder + files[:-4] + str(len(im)) + '_colors_3D.png', dpi=90, bbox_inches='tight')
    # plt.show()
    plt.close(fig)


def load_pantone_data(pantone_path):
  # print("Loading Pantone data into memory...")
    pantone_data = pd.read_excel(pantone_path, header=0)

    def convert_rgb(value):
        if isinstance(value, str):  # 如果是字符串，转换为列表
            return list(map(int, value.split(',')))
        elif isinstance(value, list):  # 如果已经是列表，直接返回
            return value
        elif isinstance(value, int):  # 如果是整数（可能是意外值），包裹成列表
            value_str = str(value)[::-1]  # 将整数转换为字符串并反转
            chunks = [int(value_str[i:i+3][::-1]) for i in range(0, len(value_str), 3)]  # 每 3 位切分并反转回来
            return chunks[::-1]  # 切分好的列表再反转回来，从左到右排列
        else:
            raise ValueError(f"Unexpected RGB format: {value}")
    
    pantone_data["RGB"] = pantone_data["RGB"].apply(convert_rgb)
    return pantone_data


def find_pantone(p2, pantone_data):
    color_dis = pantone_data["RGB"].apply(lambda x: calculate_color_distance(x, p2))
    closest_index = color_dis.idxmin()
    closest_pantone = pantone_data.loc[closest_index]
    return {
        "Pantone Code": closest_pantone["Pantone Code"],
        "Pantone Name": closest_pantone["Pantone Name"],
        "Pantone RGB": closest_pantone["RGB"]
    }


# def generate_color_palette_rgb(im, k):
#     ##### only has RGB value 
#     # k-means for color reduction
#     temp_im = cv2.cvtColor(im, cv2.COLOR_BGR2LAB)  # convert to LAB
#     temp_im = temp_im.reshape((-1, 3))
#     k_colors = KMeans(n_clusters=k)
#     k_colors.fit(temp_im)
#     labels = k_colors.predict(temp_im)
#     cluster_colors = k_colors.cluster_centers_

#     img0 = np.ones((2, 2), dtype=np.uint8)
#     rgb_img = cv2.cvtColor(img0, cv2.COLOR_GRAY2RGB)  # convert to rgb
#     cluster_rgb = []
#     for i in cluster_colors:
#         l, a, b = (i[0], i[1], i[2])
#         rgb_img[:, :, :] = (l, a, b)
#         RGB = cv2.cvtColor(rgb_img, cv2.COLOR_LAB2RGB)  # or cv2.COLOR_HSV2RGB)
#         cluster_rgb.append(RGB[1, 1, :].tolist())

#     # Count occurrences of each label
#     label_counts = Counter(labels)

#     # Sort clusters by the number of pixels assigned to them
#     sorted_indices = [label for label, count in label_counts.most_common()]

#     # Sort cluster_rgb based on sorted_indices
#     sorted_cluster_rgb = [cluster_rgb[i] for i in sorted_indices]
    
#     return cluster_rgb, sorted_cluster_rgb, labels

def generate_color_palette(im, k):
    #### include both RGB and Pantone 
    pantone_path = '/home/zoe/ResearchProjects/DesignGenerationVector/resources/pantone.xls'
    pantone_data = load_pantone_data(pantone_path)

    # Step 1: K-Means 聚类提取颜色
    temp_im = cv2.cvtColor(im, cv2.COLOR_BGR2LAB)  # 转换到 LAB 色彩空间
    temp_im = temp_im.reshape((-1, 3))
    k_colors = KMeans(n_clusters=k)
    k_colors.fit(temp_im)
    labels = k_colors.predict(temp_im)
    cluster_colors = k_colors.cluster_centers_

    # Step 2: 转换为 RGB 颜色
    img0 = np.ones((2, 2), dtype=np.uint8)
    rgb_img = cv2.cvtColor(img0, cv2.COLOR_GRAY2RGB)  # 转换到 RGB 空间
    cluster_rgb = []
    for i in cluster_colors:
        l, a, b = (i[0], i[1], i[2])
        rgb_img[:, :, :] = (l, a, b)
        RGB = cv2.cvtColor(rgb_img, cv2.COLOR_LAB2RGB)
        cluster_rgb.append(RGB[1, 1, :].tolist())

    # Step 3: 统计每个颜色的像素数量
    label_counts = Counter(labels)

    # Step 4: 根据像素数量对聚类结果排序
    sorted_indices = [label for label, count in label_counts.most_common()]
    sorted_cluster_rgb = [cluster_rgb[i] for i in sorted_indices]

    # Step 5: 匹配 Pantone 信息
    pantone_matches = [find_pantone(rgb, pantone_data) for rgb in sorted_cluster_rgb]

    return cluster_rgb, sorted_cluster_rgb, pantone_matches, labels


def show_color_blocks_basic(cluster_rgb, name):
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

    
def show_color_blocks(cluster_rgb, name, pantone_matches):
    """
    显示颜色块（包含 RGB 值和 Pantone 信息），并保存为图片。

    Args:
        cluster_rgb (list): RGB颜色列表。
        name (str): 保存图片的路径。
        pantone_matches (list): 每个颜色对应的 Pantone 信息列表。
    """
    # 设置颜色块的总体布局参数
    width = 2.5  # 图片宽度
    height = 4   # 图片高度
    block_height = 0.4  # 每个颜色块的高度
    block_width = 1.2   # 每个颜色块的宽度
    gap_height = 0.1    # 每个颜色块之间的间距
    font_size = 8       # 字体大小

    # 创建绘图对象
    color_fig = plt.figure(figsize=(width, height))
    box = color_fig.add_subplot(111)

    # 遍历颜色块和 Pantone 信息，逐一绘制
    for i, (color, pantone) in enumerate(zip(cluster_rgb, pantone_matches)):
        # 计算绘制位置
        face_color = tuple(np.array(color) / 255)  # 将 RGB 转为 matplotlib 可用的 [0, 1] 范围
        loc_y = -i * (block_height + gap_height) - 0.5  # 每块颜色的起始位置

        # 绘制颜色块
        tmp_box = plt.Rectangle((-0.3, loc_y), block_width, block_height, facecolor=face_color, 
                                 edgecolor='gray', linewidth=0.1, fill=True)
        box.add_patch(tmp_box)

        # 添加文字说明（包括 RGB 值和 Pantone 信息）
        rgb_text = f"RGB: {color}"
        pantone_text = f"Pantone: {pantone['Pantone Code']} ({pantone['Pantone Name']})"
        plt.text(1.0, loc_y + block_height / 2, rgb_text, fontsize=font_size, va='center', ha='left')
        plt.text(1.0, loc_y + block_height / 4 - gap_height / 2, pantone_text, fontsize=font_size - 1, va='center', ha='left', color='darkgray')

    # 设置绘图范围和隐藏坐标轴
    plt.xlim(-0.5, 2)
    plt.ylim(-height - 0.5, 0)
    plt.axis('off')

    # 保存图片
    color_fig.savefig(name, bbox_inches='tight', pad_inches=0.1)
    plt.close(color_fig)