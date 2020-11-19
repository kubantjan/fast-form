import cv2
import numpy as np


def add_black_points(img1, img2):
    size1 = img1.shape
    size2 = img2.shape

    x_shape = max(size1[0], size2[0])
    y_shape = max(size1[1], size2[1])

    empty_new_image = np.zeros((x_shape, y_shape)) + 255

    img1_new = empty_new_image.copy()
    img1_new[:size1[0], :size1[1]] = img1

    img2_new = empty_new_image.copy()
    img2_new[:size2[0], :size2[1]] = img2

    return img1_new, img2_new


def resize_appropriately(image, template):
    return add_black_points(image, template)
