#!/usr/bin/env python2

import numpy
import os
import sys
from matplotlib import pyplot as plt
from scipy.misc import imread, imshow


image_index = 1


def print_progress(progress, total):
    sys.stderr.write('{}{:3.0f}% completed.{}'.format('\r' if progress != 0 else '', 100.0 * progress / total, '\n' if progress == total else ''))


def detect_skin(image):
    CbC = numpy.array([0.5, -0.4187, -0.0813])
    CrC = numpy.array([-0.1687, -0.3313, 0.5])
    h, w, c = numpy.shape(image)
    assert c >= 3
    result = numpy.ndarray((h, w, c))
    for y in range(h):
        print_progress(y, h)
        for x in range(w):
            rgb = image[y, x, :3]
            r, g, b = tuple(rgb)
            cb = numpy.dot(CbC, rgb)
            cr = numpy.dot(CrC, rgb)
            if cr <= -0.0615369:
                if cb <= 0.0678488:
                    if cb <= 0.0352417:
                        score = 0
                    elif b <= 0.686631:
                        score = 0
                    else:
                        score = 1
                elif cb <= 0.185183:
                    score = 1
                else:
                    score = 0
            elif cr <= -0.029597:
                if cb <= 0.0434402:
                    score = 0
                elif g <= 0.168271:
                    score = 0
                else:
                    score = 1
            else:
                score = 0
            result[y, x, :3] = score
    print_progress(h, h)
    result[:, :, 3:] = 1
    return result


def skin_color_detection(image):
    skin_mask = detect_skin(image)
    global image_index
    plt.figure(image_index)
    plt.subplot(121)
    plt.imshow(skin_mask)
    plt.subplot(122)
    plt.imshow(image)
    image_index += 1


if __name__ == '__main__':
    path = '.'
    file_dir = os.listdir(path)
    for i in file_dir:
        s = os.path.splitext(i)
        if s[1] != '.py' and s[1] != '':
            print('Processing ' + s[0] + s[1] + ' ...')
            image_filename = s[0] + s[1]
            image = imread(image_filename) / 255.0
            skin_color_detection(image)
    plt.show()
