# -*- coding:utf-8 -*-
import cv2
import os
from setting import savePath, imgPath, elementPath, processPath, svgPath


def resize_img(img, scale_percent):
    """resize image"""
    scale_percent = scale_percent  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img


def process_image(image_path):
    # Implement your image processing logic here
    image = cv2.imread(image_path)
    # Process the image
    print(f"Processing {image_path}")
    # process
    return image

def process_images_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            process_image(image_path)

