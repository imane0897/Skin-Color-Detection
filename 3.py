import os
import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

image_index = 0
total_correction = 0


def print_progress(progress, total):
    sys.stderr.write('{}{:3.0f}% completed.{}'.format('\r' if progress !=
                                                      0 else '', 100.0 * progress / total, '\n' if progress == total else ''))


def cr_otsu(image, correct_image):
    """YCrCb颜色空间的Cr分量+Otsu阈值分割"""
    img = cv2.imread(image, cv2.IMREAD_COLOR)
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    c_image = cv2.imread(correct_image)

    (y, cr, cb) = cv2.split(ycrcb)
    cr1 = cv2.GaussianBlur(cr, (5, 5), 0)
    _, skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # cv2.namedWindow("image raw", cv2.WINDOW_NORMAL)
    # cv2.imshow("image raw", img)
    # cv2.namedWindow("image CR", cv2.WINDOW_NORMAL)
    # cv2.imshow("image CR", cr1)
    # cv2.namedWindow("Skin Cr+OTSU", cv2.WINDOW_NORMAL)
    # cv2.imshow("Skin Cr+OTSU", skin)

    # dst = cv2.bitwise_and(img, img, mask=skin)
    # cv2.namedWindow("seperate", cv2.WINDOW_NORMAL)
    # cv2.imshow("seperate", dst)

    shape = skin.shape
    total_same = 0
    for row in range(shape[0]):
        for col in range(shape[1]):
            if (skin[row][col] == 0 and c_image[row][col][0] == 0) or (skin[row][col] == 255 and c_image[row][col][0] == 255):
                total_same += 1
    correction = total_same / (row * col)
    global total_correction
    total_correction += correction
    global image_index
    image_index += 1
    print(correction)


if __name__ == '__main__':
    path = 'Face_Dataset/'
    file_dir = os.listdir(path + 'test_image')
    for i in file_dir:
        s = os.path.splitext(i)
        if s[1] != '.py' and s[1] != '':
            print('Processing ' + s[0] + s[1] + ' ...')
            cr_otsu(path + 'test_image/' +
                    s[0] + s[1], path + 'test_mask/' + s[0] + '.png')
    # plt.show()
    # image_path = 'Face_Dataset/test_image/amida-belly-dancer.jpg'
    # correct_image = 'Face_Dataset/test_mask/amida-belly-dancer.png'
    # skin_color_detection(image_path, correct_image)

    print(total_correction / image_index)
