# -*- coding:utf-8 -*-
import os
import time
from random import randint as ri
import lxml.etree as ET
from xml.dom import minidom
from shutil import copyfile
import re
import numpy as np
import xlrd

from utils.func_random import random_bk_rect, random_process_path
from utils.func_read import read_svg, Hex2Rgb, RGB_to_Hex
from utils.func_generate import generate_new_svg
from utils.stripe_generate import stripe_generate
from utils.check_generate import check_generate
from utils.ColorPalettePredict import ColorPalettePredict
from utils.design_generation import design_generate

import webbrowser
import cairosvg

inputPath = 'doc/input-de-vectors/'
outputPath = 'doc/outputVector/'
outputStripe = 'doc/outputStripe/'
outputCheck = 'doc/outputCheck/'
colorPath = 'doc/ref/'
tmpPath = 'doc/temp/'

if not os.path.exists(tmpPath):
    os.makedirs(tmpPath)

# import sys
# if sys.platform.startswith("win"):
#     print("当前系统是Windows")
# elif sys.platform.startswith("linux"):
#     print("当前系统是Linux")
# elif sys.platform.startswith("darwin"):
#     print("当前系统是Mac OS")
# else:
#     print("当前系统是其他操作系统")


def random_process(rect_color, height, width, pathes, files, svg_header):
    """
    random process existing vector element, and generate to new ones
    :param rect_color:
    :param height:
    :param width:
    :param pathes:
    :param files:
    :param svg_header:
    :return: new vector design's savename
    """
    new_bk_rect = random_bk_rect(rect_color, height, width)
    pathes_new = []
    for path in pathes:
        path_new = random_process_path(path, height, width)
        pathes_new.append(path_new)
    savename = outputPath + files[:-4] + '_new.svg'  # need to modify
    generate_new_svg(savename, svg_header, pathes_new, new_bk_rect)

    return savename


def str_replace(data, info):
    p = info[0]
    q = info[1]
    data2 = data.replace(p, q)
    return data2


def main(motif, stripe, check, visualization, rasterization):
    if motif:
        with open(outputPath + "motif_timecost.txt", "a") as f:
            f.write('start time:' + str(round(time.time(), 1)) + '\n')
            f.close()

        for files in os.listdir('./' + inputPath):
            temp_folder = tmpPath + files[:-4] + '/'
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)

            sub_output_folder = outputPath + files[:-4] + '/'
            if not os.path.exists(sub_output_folder):
                os.makedirs(sub_output_folder)

            svg_name = inputPath + files
            color_info_, header, height, width, bk_hex, pathes = read_svg(svg_name, temp_folder)
            colornum = len(color_info_)
            # print(color_info_)

            """1. random process"""
            # savename = random_process(bk_hex, height, width, pathes, files, header)

            """2. follow color palette"""
            for ff in os.listdir(colorPath):
                image_name = colorPath + ff
                color_palette_info = ColorPalettePredict(image_name, ff, colornum, temp_folder)
                # print(color_palette_info)

                color_pair = []
                for n in range(colornum):
                    color_pair.append([color_info_[n][0], RGB_to_Hex(color_palette_info[n][2])])
                # print(color_pair)

                """change color"""
                savename = sub_output_folder + files[:-4] + '_' + ff[:-4] + '_new.svg'
                copyfile(svg_name, savename)
                fin = open(savename, 'rt')
                data = fin.read()

                for i in range(colornum):
                    info = color_pair[i]
                    data2 = str_replace(data, info)
                    data = data2

                fin.close()
                fin = open(savename, 'wt')
                fin.write(data)
                fin.close()

                if visualization:
                    webbrowser.open(savename)
                    time.sleep(2)
                    os.system('taskkill /im firefox.exe /f')

                """new design generation"""
                try:
                    design_generate(width, height, sub_output_folder, savename)
                except Exception as e:
                    pass
        with open(outputPath + "motif_timecost.txt", "a") as f:
            f.write('finish time:' + str(round(time.time(), 1)) + '\n')
            f.close()

    if stripe:
        temp_folder = tmpPath + 'stripe/'
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        with open(outputStripe + "stripe_timecost.txt", "a") as f:
            f.write('start time:' + str(round(time.time(), 1)) + '\n')
            f.close()


        a = 1
        while a < 20:  # loop times == 20
            n = ri(2, 10)
            for ff in os.listdir(colorPath):
                image_name = colorPath + ff
                color_palette_info = ColorPalettePredict(image_name, ff, n, temp_folder)
                na = ff[5:-4]
                stripe_generate(width=100, height=100, num=n, color=color_palette_info, na=na, a=a, outputStripe=outputStripe)
            a += 1

        with open(outputStripe + "stripe_timecost.txt", "a") as f:
            f.write('finish time:' + str(round(time.time(), 1)) + '\n')
            f.close()

    if check:
        temp_folder = tmpPath + 'check/'
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)

        with open(outputCheck + "check_timecost.txt", "a") as f:
            f.write('start time:' + str(round(time.time(), 1)) + '\n')
            f.close()

        a = 1
        while a < 1:  # loop times == 20
            # n = ri(2, 8)
            n = 3
            for ff in os.listdir(colorPath):
                image_name = colorPath + ff
                color_palette_info = ColorPalettePredict(image_name, ff, n, temp_folder)
                na = ff[5:-4]
                check_generate(width=100, height=100, num=n,
                               color=color_palette_info,
                               na=na, a=a, outputCheck=outputCheck)
            a += 1

        with open(outputCheck + "check_timecost.txt", "a") as f:
            f.write('final time:' + str(round(time.time(), 1)) + '\n')
            f.close()

    if rasterization:
        png_folder = 'doc/GeneratedPng/'
        if not os.path.exists(png_folder):
            os.makedirs(png_folder)

        vec_folder = 'doc/all-vector-de/'
        if not os.path.exists(vec_folder):
            os.makedirs(vec_folder)

        # """move svg files"""
        # for curDir, dirs, files in os.walk('doc/outputVector_v2/'):
        #     for dir in dirs:
        #         for svg in os.listdir(os.path.join(curDir + dir)):
        #             ori = 'doc/outputVector_v2/' + dir + '/' + svg
        #             savename = vec_folder + svg
        #             copyfile(ori, savename)
        #
        # vecFolder = ['doc/outputCheck/', 'doc/outputStripe/']
        # for ff in vecFolder:
        #     for svg in os.listdir(ff):
        #         ori = ff + svg
        #         savename = vec_folder + svg
        #         copyfile(ori, savename)

        """svg --> png"""
        for fi in os.listdir(vec_folder):
            try:
                temppng = png_folder + fi[:-4] + '.png'
                tempsvg = vec_folder + fi
                cairosvg.svg2png(url=tempsvg, write_to=temppng)
            except Exception as e:
                pass

        # for folder in [inputPath, outputCheck, outputStripe]:
        #     for files in os.listdir('./' + folder):
        #         try:
        #             temppng = folder + files[:-4] + '.png'
        #             tempsvg = folder + files
        #             cairosvg.svg2png(url=tempsvg, write_to=temppng)
        #         except Exception as e:
        #             pass
        #
        # temp_folder = tmpPath + 'GeneratedPng/'
        # if not os.path.exists(temp_folder):
        #     os.makedirs(temp_folder)
        #
        # for curDir, dirs, files in os.walk(outputPath):
        #     for i in dirs:
        #         for fi in os.listdir(curDir + i + '/'):
        #             try:
        #                 temppng = temp_folder + i + fi[:-4] + '.png'
        #                 tempsvg = curDir + i + '/' + fi
        #                 cairosvg.svg2png(url=tempsvg, write_to=temppng)
        #             except Exception as e:
        #                 pass


if __name__ == '__main__':
    print("start!!!")
    main(motif=False, stripe=False, check=True, visualization=False, rasterization=False)
    print("finish!!!")




