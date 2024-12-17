# -*- coding:utf-8 -*-

import numpy as np
import potrace
import cv2
import os
from PIL import Image


# # 创建一个包含矩形的 numpy 数组
# data = np.zeros((32, 32), np.uint32)
# data[8:32-8, 8:32-8] = 1

# # 从数组创建位图
# bmp = potrace.Bitmap(data)

# # 将位图转换为路径
# path = bmp.trace()

# # 初始化 SVG 内容
# svg_content = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="320" height="320">'

# # 遍历路径曲线
# for curve in path:
#     d = f"M {curve.start_point[0]} {curve.start_point[1]} "
#     for segment in curve:
#         if segment.is_corner:
#             d += f"L {segment.c[0]} {segment.c[1]} "
#         else:
#             d += f"C {segment.c1[0]} {segment.c1[1]}, {segment.c2[0]} {segment.c2[1]}, {segment.end_point[0]} {segment.end_point[1]} "
#     d += "Z"  # 关闭路径
#     svg_content += f'<path d="{d}" fill="none" stroke="black" />'

# svg_content += '</svg>'

# # 将 SVG 内容保存到本地文件
# with open("test/test.svg", "w") as file:
#     file.write(svg_content)





# 读取图像
image_path = "/home/zoe/ResearchProjects/DesignGenerationVector/data/temp/process/test_0colormask_9.png"
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# 应用二值化
_, binary_image = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)

# 保存二值图像
output_path = "/home/zoe/ResearchProjects/DesignGenerationVector/data/temp/process/test_0colormask_9.bmp"
cv2.imwrite(output_path, binary_image)

os.system('potrace ' + output_path + ' -b svg')