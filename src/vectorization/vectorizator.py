# -*- coding:utf-8 -*-
import sys
sys.path.append('/home/zoe/ResearchProjects/DesignGenerationVector')
import math
import setting
from sklearn.cluster import KMeans
import time
import numpy as np
from random import randint as ri
import cv2  # 3.4.2
import imutils

import os
import cairosvg
from matplotlib import pyplot as plt

from setting import savePath, imgPath, elementPath, processPath, keepPath, svgPath, colorrefPath

from utils.colorize_functions import (colorize_histogram, show_color_blocks, calculate_color_distance, 
                                rgb_to_hex, generate_color_palette)
from .vectorize_functions import (create_temp_svg, vectorize_color_region)



import warnings
warnings.filterwarnings("ignore")


def create_mapping(A, B, C):
    # Create a mapping from sorted A to C using B as intermediate
    return {tuple(a): mapping for a, mapping in zip(A, C)}

def find_corresponding_color(value, mapping):
    # Find the corresponding C value for the given A value
    return mapping.get(tuple(value))


def generate_svg(width, height, viewBox, filename, bkrecg, Path_order):
    header = '<svg version="1.0" xmlns="http://www.w3.org/2000/svg" \n' \
             'width="' + str(width) + '" height="' + str(height) + '" viewBox="' + str(viewBox) + '"' + '\n' \
             'preserveAspectRatio = "xMidYMid meet" >'

    with open(filename, 'w') as svg:
        svg.write('<?xml version="1.0" standalone="no"?>\n'
                  '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n'
                  ' "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
        svg.write(header + '\n')
        svg.write('<metadata>\n'
                  'Created by ZoeQU, 2022\n'
                  '</metadata>\n')
        svg.write(bkrecg + '\n')  # add rectangle in bk color
        for k in Path_order:
            svg.write(k[1] + '\n')
        svg.write("</svg>")
    svg.close()


def vectorize_design_element(name, keep_elements, bk_color, color_img, visualization):
    if len(keep_elements) > 0:
        element_pathes = []
        for im in keep_elements:
            im = im.astype('uint8')
            im_size = (im.shape[0], im.shape[1])  # w,h
            if im.shape[0] < 100 and im.shape[1] < 100:
                im = cv2.resize(im, (2 * im.shape[1], 2 * im.shape[0]), interpolation=cv2.INTER_CUBIC)

            im = cv2.fastNlMeansDenoisingColored(im, None, 5, 5, 3, 7)  # Denoise
            # adaptive calculate 'k'
            img_gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
            k = colorize_histogram(img_gray, name, visualization)

            # # k-means for color reduction
            cluster_rgb, sorted_cluster_rgb, labels = generate_color_palette(im, k)

            # generate color palette from input color_ref image
            if color_img is not None:
                color, sorted_color, _ = generate_color_palette(color_img, k) 
                color_block_path = processPath + 'motif_' + str(k) + '_color_blocks.png'
                show_color_blocks(sorted_color, color_block_path)

                mapping = create_mapping(sorted_cluster_rgb, cluster_rgb, sorted_color)

                # find bk_color
                distance_value = []
                for color_i in cluster_rgb:
                    distance_value.append([color_i, calculate_color_distance(bk_color, color_i)])
                distance_value = sorted(distance_value, key=lambda x: x[1])
                a = distance_value[0][0]
                ind = cluster_rgb.index(a)
                bk_color_2 = [bk_color, cluster_rgb[ind]]
                if visualization:
                    show_color_blocks(bk_color_2, processPath + name + '_2_bk_colors.png')
                    
                bk_color = cluster_rgb[ind]

                # show color blocks
                if visualization:
                    show_color_blocks(cluster_rgb, processPath + name + '_color_blocks.png')
            else:
                color_block_path = None


            # separate by color 
            colors = []
            color_and_imgs = []
            for label in np.unique(labels):
                color = cluster_rgb[label]  # rgb

                img_af_cluster = labels.copy()
                if color != [0, 0, 0]:
                    img_af_cluster = np.where(img_af_cluster == label, np.array(cluster_rgb[label]).reshape(3, 1),
                                            np.array([0, 0, 0]).reshape(3, 1))
                else:
                    img_af_cluster = np.where(img_af_cluster == label, np.array(cluster_rgb[label]).reshape(3, 1),
                                            np.array([255, 255, 255]).reshape(3, 1))

                r = np.reshape(img_af_cluster[0], (im.shape[0], im.shape[1]))
                g = np.reshape(img_af_cluster[1], (im.shape[0], im.shape[1]))
                b = np.reshape(img_af_cluster[2], (im.shape[0], im.shape[1]))
                merged = cv2.merge([r, g, b])  # 3D color image
                color_and_imgs.append([color, merged])

                if visualization:
                    plt.imshow(merged)
                    plt.axis('off')
                    plt.savefig(processPath + name + 'colormask' + str(ri(0,9)) + '.png', bbox_inches='tight', facecolor='none', edgecolor='none')
                    plt.close('all')

                # get color_mask_binary 
                temp_ = np.where(merged == color, [0, 0, 0], [255, 255, 255])  # 3 channel black & white image
                gray_image = cv2.cvtColor(temp_.astype(np.uint8), cv2.COLOR_BGR2GRAY)
                ret, color_mask_binary = cv2.threshold(gray_image, 50, 255, cv2.THRESH_BINARY)
                 
                colors.append([color, color_mask_binary])

            if visualization:
                plt.figure(figsize=(20, 8))
                for i, image in enumerate(color_and_imgs):
                    plt.subplot(2, 10, i+1)
                    plt.imshow(image[1])
                    plt.title(str(image[0]))
                    plt.axis('off')
                plt.savefig(processPath + name + '_kmean.png', bbox_inches='tight', facecolor='none', edgecolor='none')
                # plt.show()
                plt.close('all')

            # svg's header
            width = str(im.shape[1]) + '.000000pt'
            height = str(im.shape[0]) + '.000000pt'
            viewBox = '0 0 ' + width[:-2] + ' ' + height[:-2]

            # generate svg's background path
            if color_img is not None:
                bk_color_hex = rgb_to_hex(find_corresponding_color(bk_color, mapping))
            else:
                bk_color_hex = rgb_to_hex(bk_color)

            bkrecg = '<rect width="' + str(width[:-2]) + '" height="' + str(height[:-2]) \
                    + '" fill="' + str(bk_color_hex) + '"/>'
            temppng = svgPath + name + '_bk.png'
            tempsvg = create_temp_svg(bkrecg, width, height, viewBox)
            cairosvg.svg2png(url=tempsvg, write_to=temppng)
            temp_ = cv2.imread(temppng)
            a_num = np.where(temp_ == bk_color)
            bk_color_amount = len(a_num[0])

            os.remove(tempsvg)  # remove temp bk.svg 
            os.remove(temppng)  # remove temp bk.png 

            # vectorize each color region
            pathes = []
            for q in range(len(colors)):
                if rgb_to_hex(colors[q][0]) != bk_color_hex:
                    
                    if color_img is not None:
                        fillcolor=rgb_to_hex(find_corresponding_color(colors[q][0], mapping))
                    else:
                        fillcolor = rgb_to_hex(colors[q][0])

                    color_mask_bmp = svgPath + name + '_color_' + str(q) + '.bmp'
                    cv2.imwrite(color_mask_bmp, colors[q][1])

                    path_strings = vectorize_color_region(color_mask_bmp, fillcolor)

                    if len(path_strings) > 0:
                        for j in range(len(path_strings)):
                            path_i = '<path d="' + str(path_strings[j]) + '" transform="translate(0.000000,' + str(
                                height[:-2]) + ')' \
                            ' scale(0.100000,-0.100000)" stroke="none" ' \
                            'fill="' + fillcolor + '"/>\n'
                            pathes.append(path_i)
                    os.remove(color_mask_bmp)
                    os.remove(color_mask_bmp[:-4] + '.svg')

            # order path by area, small->large| path_area by calculate black pixel
            p_order = []
            p_ori = []
            for pi in pathes:
                tempname = create_temp_svg(pi, width, height, viewBox)  # pi is path
                temp = svgPath + 'temp.png'
                cairosvg.svg2png(url=tempname, write_to=temp)
                temp_ = cv2.imread(temp)

                # count black pixels
                h, w, _ = temp_.shape
                npim = temp_[:, :, 0] + temp_[:, :, 1] + temp_[:, :, 2]
                black_pixel_num = len(npim[npim == 0])
                content = npim.shape[0] * npim.shape[1] - black_pixel_num
                # record ori path
                p_ori.append([content, pi])

                # record path after filter
                if content > (0.002 * bk_color_amount):   # the defination of meaningless path
                    p_order.append([content, pi])
                else:
                    pass
                os.remove(tempname)
                os.remove(temp)

            path_ori = sorted(p_ori, key=lambda x: x[0])
            num_ori = len(path_ori) + 1
            path_order = sorted(p_order, key=lambda x: x[0])
            num_af_filter = len(path_order) + 1

            # generate new vector graphic
            filename_ori = svgPath + name + '_ori_num_' + str(num_ori) + '.svg'
            generate_svg(width, height, viewBox, filename_ori, bkrecg, path_ori)

            filename_filter = svgPath + name + '_filter_num_' + str(num_af_filter) + '.svg'
            generate_svg(width, height, viewBox, filename_filter, bkrecg, path_order)

            # return [im_size, filename_ori, num_ori, filename_filter, num_af_filter]
            element_pathes.append(filename_filter)
        return element_pathes, color_block_path
        
    else:
        return None
    

if __name__=="__main__":
    image_path = "/home/zoe/ResearchProjects/DesignGenerationVector/data/temp/keep/test_0.png"
    img = cv2.imread(image_path)
    print(img.shape) # (243,338,3)
    name = "test_0"
    element_pathes, color_block_path  = vectorize_design_element(name, keep_elements=[img], bk_color=[253, 240, 215], color_img=None, visualization=False)
    print("biu~biu~biu~")