# -*- coding:utf-8 -*-
import math
from sklearn.cluster import MeanShift, estimate_bandwidth, KMeans
import numpy as np
import itertools
from collections import defaultdict, Counter
import cv2  #3.4.2
# print(cv2.__version__)
import os
import re
import heapq
from PIL import Image
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def im_show(im):
    plt.imshow(im)
    plt.axis('off')
    plt.show()
    plt.cla()


def cal_distance(p1, p2):
    return math.sqrt(math.pow((p2[0] - p1[0]), 2) + math.pow((p2[1] - p1[1]), 2) + math.pow((p2[2] - p1[2]), 2))


def find_pantone(p2):
    pantone_path = './doc/pantone/tpxPantone.txt'
    with open(pantone_path, 'r') as f:
        pantone_ = f.readlines()
        pantone_info = pantone_[1:]
        pantone_code = []
        pantone_rgb = []
        pantone_name = []
        for j in range(len(pantone_info)):
            t = re.split('\t|\n', pantone_info[j])
            pantone_code.append(t[0])
            pantone_rgb.append([int(t[1].split(',')[0]), int(t[1].split(',')[1]), int(t[1].split(',')[2])])
            pantone_name.append(t[2])

    color_dis = []
    for i in pantone_rgb:
        dis = cal_distance(i, p2)
        color_dis.append(dis)

    # # 返回一个值
    ind = np.argmin(np.array(color_dis))
    code = pantone_code[int(ind)]
    name = pantone_name[int(ind)]
    # # 返回3个值
    # a = np.array(color_dis)
    # inds = heapq.nlargest(3, range(len(a)), a.take)
    # codes = []
    # names = []
    # for ind in inds:
    #     codes.append(pantone_code[ind])
    #     names.append(pantone_name[ind])
    return code, name


def color_his(img, t):
    """gray img color histogram"""
    img = img.reshape((-1, 1))
    breaks = np.linspace(np.min(img), np.max(img), 20)
    counts = {}
    for i in range(len(breaks) - 1):
        left, right = breaks[i], breaks[i + 1]
        label = f"({left:.2f}, {right:.2f}]"
        count = 0
        for val in img:
            if val > left and val <= right:
                count += 1
        counts.update({label: count})
    # keys = [k for k in counts.keys()]
    # values = [v for v in counts.values()]
    fig, ax = plt.subplots(figsize=(10, 7))
    p = ax.hist(img, bins=20, rwidth=0.85, weights=[1./len(img)]*len(img))
    # plt.axvline(int(thre), linewidth=2, linestyle="--", color='red') # vertical line
    plt.axhline(t, linewidth=2, linestyle="--", color='red') # horizontal line
    # plt.text(int(thre), 0, int(thre), fontsize=18) # add text
    # ax.set_title("Simple Histogram") # add title
    # plt.savefig(setting.SavePath + files[:-4] + '_' + "gray_color_dis_hist.png")
    # plt.show()
    plt.close()
    thre = []
    for item in p[0]:
        if item > t:
            thre.append(item)
    return len(thre)


def color_blocks(color_info, savename):
    cluster_rgb = [i[2] for i in color_info]
    """show color blocks, max 10 colors"""
    fig, axs = plt.subplots(len(cluster_rgb), 1, figsize=(15, 15))

    """add Pantone color number"""
    cluster_pantone = []
    for j in cluster_rgb:
        pantone_code, pantone_name = find_pantone(j)
        cluster_pantone.append([pantone_code, pantone_name])

    for i, color in enumerate(cluster_rgb):
        img = Image.new('RGB', (10, 10), tuple(color))
        ax = axs[i]
        l = str(cluster_pantone[i][0] + '\n' + cluster_pantone[i][1])
        ax.set_title(l, fontsize=12)
        # ax.set_xticks([])
        # ax.set_yticks([]) # 去掉坐标轴　　
        ax.axis('off')
        ax.imshow(img)
    plt.savefig(savename, dpi=90, bbox_inches='tight')
    # plt.show()
    plt.close()

    # color_fig = plt.figure()
    # box = color_fig.add_subplot(111, aspect='equal')
    # for i in range(len(cluster_rgb)):
    #     face_color = tuple(np.array(cluster_rgb[i])/255)
    #     loc_x = i * 0.1
    #     Loc = tuple([loc_x, 0])
    #     tmp_box =plt.Rectangle(Loc, 0.1,0.8,facecolor=face_color,edgecolor='r',fill=True)
    #     box.add_patch(tmp_box)
    #     plt.text(loc_x, 0.95, "["+str(cluster_rgb[i][0]))
    #     plt.text(loc_x, 0.9, str(cluster_rgb[i][1]))
    #     plt.text(loc_x, 0.85, str(cluster_rgb[i][2])+"]")
    # plt.axis('off')
    # color_fig.savefig(savename, dpi=90, bbox_inches='tight')
    # # plt.show()
    # plt.close(color_fig)


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
    plt.savefig(temp_folder + files[:-4] + '_colors_3D.png', dpi=90, bbox_inches='tight')
    # plt.show()
    plt.close(fig)


def merge_color(CC):
    Keep = []
    Merge = []
    for c in CC:
        M = []
        M.append(c)
        for x in CC[1:]:
            if cal_distance(c[2], x[2]) < 45:
                M.append(x)
        for a in M:
            try:
                CC.remove(a)
            except Exception as e:
                continue
        Merge.append(M)
    Keep.append(CC)

    Left = []
    for j in Merge:
        jj = sorted(j, key=lambda k: k[1])
        Left.append(jj[-1])
    for p in Keep[0]:
        Left.append(p)

    cluster_colors2 = [x[2] for x in Left]
    return cluster_colors2


def list_duplicates(seq):
    pairs = [[x[0][0], x[1][0]] for x in seq]
    l = pairs[0]
    temp = pairs[1:]
    l2 = []
    for pair in temp:
        a = [y for y in pair if y in l]
        if len(a) > 0:
            l += pair
        else:
            l2.append(pair)


def ColorPalettePredict(image_name, files, colornum, temp_folder):
    """
    read image and generate its corresponding color palette
    :param image_name: color ref img
    :param files: the name of the ref img, for save temp results
    :param colornum: kmeans k
    :param temp_folder: temp imgs path
    :return:
    """
    im = cv2.imread(image_name)

    """cluster color"""
    temp_im = cv2.cvtColor(im, cv2.COLOR_BGR2LAB)  # LAB optional, / cv2.COLOR_BGR2HSV)
    temp_in = temp_im.reshape((-1, 3))

    """kmeans for color clustering"""
    Kcolor = KMeans(n_clusters=colornum)
    Kcolor.fit(temp_in)
    labels = Kcolor.predict(temp_in)
    cluster_colors = Kcolor.cluster_centers_
    labels = labels.tolist()

    color_info = []
    for i in range(len(cluster_colors)):
        color_info.append([i, labels.count(i), cluster_colors[i].tolist()])

    """convert to RGB"""
    img0 = np.ones((2, 2), dtype=np.uint8)
    rgb_img = cv2.cvtColor(img0, cv2.COLOR_GRAY2RGB)  # rgb
    for j in color_info:
        i = j[2]
        l, a, b = (i[0], i[1], i[2])
        rgb_img[:, :, :] = (l, a, b)
        RGB = cv2.cvtColor(rgb_img, cv2.COLOR_LAB2RGB)  # / cv2.COLOR_HSV2RGB)
        j[2] = RGB[0][0]

    """show pixel in 3d"""
    cluster_rgb = [i[2] for i in color_info]
    color3dshow(cluster_rgb, temp_folder, files)

    """show color blocks"""
    savename = temp_folder + files[:-4] + '_colors.png'
    color_blocks(color_info, savename)

    """show color palette"""
    im2 = cv2.imread(savename)

    if im.shape[1] / im.shape[0] > 1.1:
        im2 = np.rot90(im2)
        im2 = cv2.resize(im2, (im.shape[1], int(im.shape[1] / 4)))
        img = cv2.vconcat([im.astype('int32'), im2.astype('int32')])
    else:
        im2 = cv2.resize(im2, (int(im.shape[0]/4), im.shape[0]))
        img = cv2.hconcat([im.astype('int32'), im2.astype('int32')])
    cv2.imwrite(temp_folder + files[:-4] + '_colorpalette.png', img)

    color_info = sorted(color_info, key=lambda x: x[1])
    return color_info



