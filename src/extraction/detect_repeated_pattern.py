# -*- coding:utf-8 -*-
import sys
sys.path.append('/home/zoe/ResearchProjects/DesignGenerationVector')
import numpy as np
import cv2
import os
import time
from matplotlib import pyplot as plt
from matplotlib import colors
from PIL import Image, ImageDraw

from setting import savePath, imgPath, elementPath, processPath, keepPath, svgPath, colorrefPath


#TODO(Zoe 17 Nov)
def grid_draw(image_path, dstar):
    save_name = processPath + name + '_grid.png'
    start = [0, 0]
    img = Image.open(image_path)
    img = img.convert('RGB')
    img_d = ImageDraw.Draw(img)
    x_len, y_len = img.size
    if dstar[0] != x_len:
        for x in range(start[0], x_len, dstar[0]):
            img_d.line(((x, 0), (x, y_len)), fill=(255, 0, 0), width=2)
    if dstar[1] != y_len:
        for y in range(start[1], y_len, dstar[1]):
            img_d.line(((0, y), (x_len, y)), fill=(255, 0, 0), width=2)
    # img.show()
    img.save(save_name)


def sim_curve(resx, savename, title):
    """plot similarity curve"""
    x = list(range(resx.shape[1]))
    y = resx.tolist()[0]
    plt.figure(figsize=(10, 8))
    plt.plot(x, y, color="red", linewidth=1, linestyle="--")
    plt.xlabel("pixel")
    plt.ylabel("sim")
    plt.title(title)
    plt.savefig(savename, dpi=120, bbox_inches='tight')
    plt.show()
    plt.close()


def crop_x(img, dstar):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = img_gray[:dstar[1], :dstar[0]]
    img_x = img_gray[:dstar[1], int(dstar[0] / 3):]
    return template, img_x


def refine(img, template, dstar, similarity):
    resx = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    resx = np.reshape(resx, (1, -1))
    mu = np.average(resx, axis=1)
    threshold = np.max(resx) * similarity
    loc_x = np.where(resx >= threshold)

    if len(loc_x[1]) < 2:
        threshold_w = np.max(resx)
        loc_x = np.where(resx >= threshold_w)
        dstar_x = loc_x[1]
        dstar_w = dstar_x + int(dstar[0] / 3)
        return dstar_w, mu, resx

    else:
        for ii in range(len(loc_x[1]) - 1):
            if loc_x[1][ii + 1] - loc_x[1][ii] < 2:
                dstar_x = loc_x[1][ii + 1]
                dstar_w = dstar_x + int(dstar[0] / 3)
                return dstar_w, mu, resx

            else:
                dstar_x = loc_x[1][ii]
                if dstar_x < 10:
                    continue
                dstar_w = dstar_x + int(dstar[0] / 3)
                return dstar_w, mu, resx


def crop_y(img, dstar):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = img_gray[:dstar[0], :dstar[1]]
    img_y = img_gray[int(dstar[0] / 3):, : dstar[1]]
    return template, img_y


def predict_repeated_pattern_size(image_path,name, visualize):
    img = cv2.imread(image_path)
    i_h = img.shape[0]
    i_w = img.shape[1]
    dstar = [ int(i_w / 4), int(i_h / 4)]
    # # 1. refine x-axis
    similarity = 0.9

    template_x, img_x = crop_x(img, dstar)
    template_y, img_y = crop_y(img, dstar)
    dstar_x, mux, resx = refine(img_x, template_x, dstar, similarity)

    if visualize:
        savename = processPath + name + '_sim_x.png'
        title = 'similarity in x-axis'
        sim_curve(resx, savename, title)

    # # 2. refine y-axis
    dstar_y, muy, resy = refine(img_y, template_y, dstar, similarity)
    
    if visualize:
        savename = processPath + name + '_sim_y.png'
        title = 'similarity in y-axis'
        sim_curve(resy, savename, title)
    
    if dstar_x > 0.51 * i_w or dstar_y > 0.51 * i_h:
        dstar_x = i_w
        dstar_y = i_h

    dstar = [dstar_x, dstar_y]

    grid_draw(image_path, dstar)
    return dstar


if __name__ == "__main__":
    image_path = imgPath + "test.jpg"
    name = image_path.split("/")[-1].split(".")[0]
    print(name)
    dstar = predict_repeated_pattern_size(image_path, name, visualize=True)
    print(dstar)