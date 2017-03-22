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
    rows,cols,channels = img.shape
    imgYcc = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgSkin = np.zeros(img.shape, np.uint8)
    imgSkin = img.copy()

    for r in range(rows):
        print_progress(r, rows)
        for c in range(cols):
            skin = 0
            R = img.item(r,c,0)
            G = img.item(r,c,1)
            B = img.item(r,c,2)

            Y = imgYcc.item(r,c,0)
            Cr = imgYcc.item(r,c,1)
            Cb = imgYcc.item(r,c,2)

            if R > G and R > B:
                if (G >= B and 5 * R - 12 * G + 7 * B >= 0) or (G < B and 5 * R + 7 * G - 12 * B >= 0):
                    if Cr > 135 and Cr < 180 and Cb > 85 and Cb < 135 and Y > 80:
                        skin = 1

            if 0 == skin:
                imgSkin.itemset((r,c,0),0)
                imgSkin.itemset((r,c,1),0)
                imgSkin.itemset((r,c,2),0)
            else:
                imgSkin.itemset((r,c,0),255)
                imgSkin.itemset((r,c,1),255)
                imgSkin.itemset((r,c,2),255)
    print_progress(r, rows)
    global image_index
    plt.figure(image_index)
    plt.subplot(1,2,1)
    plt.imshow(img)
    plt.title('Original Image')
    plt.xticks([])
    plt.yticks([])
    plt.subplot(1,2,2)
    plt.imshow(imgSkin)
    plt.title('Transformed YCbCr Skin Image')
    plt.xticks([])
    plt.yticks([])
    image_index += 1
    print(imgFile + ' has been processed successfully!')

if __name__ == '__main__':
    path = '.'
    file_dir = os.listdir(path)
    for i in file_dir:
        s = os.path.splitext(i)
        if s[1] != '.py' and s[1] != '':
            print('Processing ' + s[0] + s[1] + ' ...')
            skin_color_detection(s[0] + s[1])
    plt.show()
