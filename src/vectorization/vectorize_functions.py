# -*- coding:utf-8 -*-
import sys
import os
sys.path.append('/home/zoe/ResearchProjects/DesignGenerationVector')
import potrace
import lxml.etree as ET
from xml.dom import minidom

from setting import savePath, imgPath, elementPath, processPath, keepPath, svgPath, colorrefPath

def create_temp_svg(path_i, width, height, viewBox):
    header = '<svg version="1.0" xmlns="http://www.w3.org/2000/svg" \n' \
             'width="' + str(width) + '" height="' + str(height) + \
             '" viewBox="' + str(viewBox) + '"' + '\n' \
            'preserveAspectRatio = "xMidYMid meet" >'
    tempname = svgPath + 'temp.svg'
    with open(tempname, 'w') as svg:
        svg.write('<?xml version="1.0" standalone="no"?>\n'
                  '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n'
                  ' "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
        svg.write(header + '\n')
        svg.write(path_i + '\n')
        svg.write("</svg>")
    svg.close()
    return tempname



def vectorize_color_region(bmp_name, hex_code):
    os.system('potrace ' + bmp_name + ' -b svg')
    tree = ET.parse(open(bmp_name[:-4] + '.svg', 'r'))
    root = tree.getroot()
    height = root.attrib['height']
    width = root.attrib['width']
    viewBox = root.attrib['viewBox']
    header = '<svg version="1.0" xmlns="http://www.w3.org/2000/svg" \n' \
             'width="' + str(width) + '" height="' + str(height) + '" viewBox="' + str(viewBox) + '"' + '\n' \
             'preserveAspectRatio = "xMidYMid meet" >'
    doc = minidom.parse(bmp_name[:-4] + '.svg')  # parseString also exists
    path_strings = [path.getAttribute('d') for path
                    in doc.getElementsByTagName('path')]
    doc.unlink()

    return path_strings