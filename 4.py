#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import __future__
import cv2
import numpy as np
from matplotlib import pyplot as plt

image_index = 1

def print_progress(progress, total):
    sys.stderr.write('{}{:3.0f}% completed.{}'.format('\r' if progress != 0 else '', 100.0 * progress / total, '\n' if progress == total else ''))


def skin_color_detection(imgFile):
    img = cv2.imread(imgFile)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rows,cols,channels = img.shape
    imgYcc = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
    print(imgYcc)
    # for r in range(rows):
    #     print_progress(r, rows)
    #     for c in range(cols):
    #         skin = 0
    #
    #         Y = imgYcc.item(r,c,0)
    #         Cr = imgYcc.item(r,c,1)
    #         Cb = imgYcc.item(r,c,2)
    #
    #         if Cr >= 133 and Cr <= 173 and Cb >= 80 and Cb <= 120:
    #             skin = 1
    #             imgYcc[r, c] = [255, 255, 255]
    #         else:
    #             imgYcc[r, c] = [0, 0, 0]

    # print_progress(r, rows)
    # global image_index
    # plt.figure(image_index)
    # plt.subplot(1,2,1)
    # plt.imshow(img)
    # plt.title('Original Image')
    # plt.subplot(1,2,2)
    # plt.imshow(imgYcc)
    # plt.title('Transformed YCbCr Skin Image')
    # image_index += 1


if __name__ == '__main__':
    path = '.'
    file_dir = os.listdir(path)
    for i in file_dir:
        s = os.path.splitext(i)
        if s[1] != '.py' and s[1] != '':
            print('Processing ' + s[0] + s[1] + ' ...')
            skin_color_detection(s[0] + s[1])
    plt.show()
