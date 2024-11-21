# -*- coding:utf-8 -*-
import sys
sys.path.append('/home/zoe/ResearchProjects/DesignGenerationVector/')
import math
from random import randint as ri
from random import uniform as rf
import lxml.etree as ET
from xml.dom import minidom
import time
import argparse
import sys
from operator import itemgetter
import itertools
from collections import defaultdict, Counter
import numpy as np
import cv2 
import imutils
import os
import cairosvg
from matplotlib import pyplot as plt

from setting import savePath, imgPath, elementPath, processPath, keepPath, svgPath, colorrefPath

from utils.colorize_functions import rgb_to_hex, hex_to_rgb, hex_random, generate_color_palette, show_color_blocks 
from .generate_functions import (generate_new_svg, rowgroup, striperowgroup, columgroup, mirror, generate_random_width, 
                                draw_sequence, cal_loc, stripe_pathes, generate_golden_pattern, pares_svg)




def generate_common_pattern(element, new_pattern_name, type, header, pattern_width, pattern_height, bk_rect, pathes_new):
    row = rowgroup(pathes_new, pattern_width / 4)
    col = columgroup(pathes_new, pattern_height / 4)

    with open(new_pattern_name, 'w') as svg:
        svg.write('<?xml version="1.0" standalone="no"?>\n'
                  '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n'
                  ' "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
        svg.write(header + '\n')
        svg.write('<metadata>\n'
                  'Created by ZoeQu, written in 2024\n'
                  '</metadata>\n')
        svg.write(bk_rect + '\n')

        if type == 'straight':
            for r in range(4):
                svg.write('<g id="row' + str(r) + '" ' + 'transform=' +
                          '"translate(' + str(int(pattern_width / 30)) +
                          ',' + str(r * pattern_height / 4) + ')' + '">' + '\n')
                for k in row:
                    svg.write(k + '\n')
                svg.write('</g>' + '\n')

        if type == 'tile':
            for r in range(4):
                if (r % 2) == 0:
                    svg.write('<g id="row' + str(r) + '" ' +
                              'transform=' + '"translate(' + str(int(pattern_width / 30)) +
                              ',' + str(r * pattern_height / 4) + ')' + '">' + '\n')
                else:
                    svg.write('<g id="row' + str(r) + '" ' + 'transform=' +
                              '"translate(' + str(int(pattern_width / 30) - int(pattern_width / 8))
                              + ',' + str(r * pattern_height / 4) + ')' + '">' + '\n')
                for k in row:
                    svg.write(k + '\n')
                svg.write('</g>' + '\n')

        if type == 'half-drop':
            for c in range(4):
                if (c % 2) == 0:
                    svg.write('<g id="col' + str(c) + '" ' + 'transform=' +
                              '"translate(' + str(int(c * pattern_width / 4)) +
                              ', ' + str(int(pattern_height / 30)) + ')' + '">' + '\n')
                else:
                    svg.write('<g id="col' + str(c) + '" ' +
                              'transform=' + '"translate(' + str(int(c * pattern_width / 4)) +
                              ', ' + str(int(pattern_height / 30) - pattern_height / 8) + ')' +
                              '">' + '\n')
                for k in col:
                    svg.write(k + '\n')
                svg.write('</g>' + '\n')

        if type == 'mirror':
            pathes_new = mirror(element, pattern_width / 4, pattern_height/ 4)
            row = striperowgroup(pathes_new, pattern_width / 4)

            for r in range(4):
                svg.write('<g id="row' + str(r) + '" ' + 'transform=' +
                          '"translate(' + str(int(pattern_width / 30)) +
                          ',' + str(r * pattern_height / 4) + ')' + '">' + '\n')
                for k in row:
                    svg.write(k + '\n')
                svg.write('</g>' + '\n')

        svg.write("</svg>")
    svg.close()



def generate_motif_pattern(element):
    pathes_new, bk_hex, width, height, num = pares_svg(element)
    
    name = element.split("/")[-1][:-4]
    pattern_width = 4 * int(width.split(".")[0])
    pattern_height = 4 * int(height.split(".")[0])
    pattern_header = '<svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="' \
                    + str(pattern_width) + 'pt" height="' + str(pattern_height) + \
                    'pt" viewBox="' + '0 0 ' + str(pattern_width) + ' ' + \
                    str(pattern_height) + '" ' + \
                    'preserveAspectRatio = "xMidYMid meet" >'

    bk_rect = '<rect width="' + str(pattern_width) + '" height="' + str(pattern_height) + \
              '" fill="' + str(bk_hex[0]) + '"/>'

    type_code = ri(0, 4)

    type_list =  ['straight', 'tile', 'half-drop', 'mirror', 'customize-golden-ratio']
    i = type_list[type_code]
    print("type code: " + i)

    if i != 'customize-golden-ratio':
        new_pattern_name = savePath + name + '_' + str(i) + '_pattern.svg'
        generate_common_pattern(element, new_pattern_name, i, pattern_header, pattern_width, pattern_height, bk_rect, pathes_new)

    else:
        aa = int(10 * max(pattern_width / 4 , pattern_height / 4)/(1.618 * 1.618))
        pattern_path, bk_color = generate_golden_pattern(aa, element)
        width2 = int(12 * aa)

        bk_rect_gold = '<rect width="' + str(width2) + '" height="' + str(width2) + \
                        '" fill="' + str(bk_color[0]) + '"/>'

        rowgroup = []
        for i in range(5):
            grouppath = '<g id="' + str(i) + '" ' + 'transform=' + '"translate(' + \
                        str(i * width2 * 0.25) + ',0)' + 'scale(0.25,0.25)' + '">' + '\n'
            rowgroup.append(grouppath)
            for j in pattern_path:
                rowgroup.append(j)
            rowgroup.append('</g>' + '\n')

        new_pattern_name = savePath + name + '_customize-golden-ratio_pattern.svg'
        header_gold = '<svg version="1.0" xmlns="http://www.w3.org/2000/svg" width="' \
                        + str(int(width2)) + 'pt" height="' + str(int(width2)) + \
                        'pt" viewBox="' + '0 0 ' + str(int(width2)) + ' ' + \
                        str(int(width2)) + '" ' + \
                        'preserveAspectRatio = "xMidYMid meet" >'
        
        with open(new_pattern_name, 'w') as svg:
            svg.write('<?xml version="1.0" standalone="no"?>\n'
                        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n'
                        ' "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
            svg.write(header_gold + '\n')
            svg.write('<metadata>\n'
                        'Created by ZoeQu, written in 2024\n'
                        '</metadata>\n')
            svg.write(bk_rect_gold + '\n')
            for r in range(4):
                svg.write('<g id="row' + str(r) + '" ' + 'transform=' +
                            '"translate(' + str(int(0)) +
                            ',' + str(r * width2 / 4) + ')' + '">' + '\n')
                for k in rowgroup:
                    svg.write(k + '\n')
                svg.write('</g>' + '\n')

            svg.write("</svg>")
        svg.close()

    return new_pattern_name
    




if __name__ == "__main__":
    element_path = "/home/zoe/ResearchProjects/DesignGenerationVector/data/temp/svg/test_filter_num_26.svg"
    new_pattern_name = generate_motif_pattern(element_path)
    print("biu~biu~biu~")