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


def skin_color_detection(image_name):
    test_image = cv2.imread(image_name)
    # RGB到YCbCr色彩空间
    image_YCbCr = cv2.cvtColor(test_image, cv2.COLOR_RGB2YCrCb)

    # 返回(行数，列数，通道个数)
    shape = image_YCbCr.shape

    Kl, Kh = 125, 188
    Ymin, Ymax = 16, 235
    Wlcb, Wlcr = 23, 20
    Whcb, Whcr = 14, 10
    Wcb, Wcr = 46.97, 38.76
    # 椭圆模型参数
    Cx, Cy = 109.38, 152.02
    ecx, ecy = 1.60, 2.41
    a, b = 25.39, 14.03
    Theta = 2.53 / np.pi * 180
    # 每行
    for row in range(shape[0]):
        # 每列
        print_progress(row, shape[0])
        for col in range(shape[1]):
            Y = image_YCbCr[row, col, 0]
            CbY = image_YCbCr[row, col, 1]
            CrY = image_YCbCr[row, col, 2]
            if Y < Kl or Y > Kh:
                # 求Cb, Cr的均值
                if Y < Kl:
                    # 公式(7)
                    CbY_aver = 108 + (Kl - Y) * (118 - 108) / (Kl - Ymin)
                    # 公式(8)
                    CrY_aver = 154 - (Kl - Y) * (154 - 144) / (Kl - Ymin)
                    # 公式(6)
                    WcbY = Wlcb + (Y - Ymin) * (Wcb - Wlcb) / (Kl - Ymin)
                    WcrY = Wlcr + (Y - Ymin) * (Wcr - Wlcr) / (Kl - Ymin)
                elif Y > Kh:
                    # 公式(7)
                    CbY_aver = 108 + (Y - Kh) * (118 - 108) / (Ymax - Kh)
                    # 公式(8)
                    CrY_aver = 154 + (Y - Kh) * (154 - 132) / (Ymax - Kh)
                    # 公式(6)
                    WcbY = Whcb + (Ymax - Y) * (Wcb - Whcb) / (Ymax - Kh)
                    WcrY = Whcr + (Ymax - Y) * (Wcr - Whcr) / (Ymax - Kh)
                # 求Cb(Kh), Cr(Kh)的均值
                CbKh_aver = 108 + (Kh - Kh) * (118 - 108) / (Ymax - Kh)
                CrKh_aver = 154 + (Kh - Kh) * (154 - 132) / (Ymax - Kh)
                # 公式(5)
                Cb = (CbY - CbY_aver) * Wcb / WcbY + CbKh_aver
                Cr = (CrY - CrY_aver) * Wcr / WcrY + CrKh_aver
            else:
                # 公式(5)
                Cb = CbY
                Cr = CrY
            # Cb，Cr代入椭圆模型8
            cosTheta = np.cos(Theta)
            sinTehta = np.sin(Theta)
            matrixA = np.array([[cosTheta, sinTehta], [-sinTehta, cosTheta]], dtype=np.double)
            matrixB = np.array([[Cb - Cx], [Cr - Cy]], dtype=np.double)
            # 矩阵相乘
            matrixC = np.dot(matrixA, matrixB)
            x = matrixC[0, 0]
            y = matrixC[1, 0]
            ellipse = (x - ecx) ** 2 / a ** 2 + (y - ecy) ** 2 / b ** 2
            if ellipse <= 1:
                # 白
                image_YCbCr[row, col] = [255, 255, 255]
                # 黑
            else:
                image_YCbCr[row, col] = [0, 0, 0]
    print_progress(row, shape[0])
    # 绘图
    original = plt.imread(image_name)
    global image_index
    plt.figure(image_index)
    plt.subplot(121)
    plt.imshow(original)
    plt.title('Original')
    plt.subplot(122)
    plt.imshow(image_YCbCr)
    plt.title('New')
    image_index += 1


if __name__ == '__main__':
    path = '.'
    file_dir = os.listdir(path)
    for i in file_dir:
        s = os.path.splitext(i)
        if s[1] != '.py' and s[1] != '':
            print('Processing ' + s[0] + s[1] + ' ...')
            skin_color_detection(s[0] + s[1])
    plt.show()
