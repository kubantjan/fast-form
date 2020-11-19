import cv2
import numpy as np
from pylsd import lsd

from fast_form.config.configuration_dataclasses import ImageCv2, ImageSiftResult


def get_image_sift_result(image: ImageCv2) -> ImageSiftResult:
    sift = cv2.SIFT_create()
    # find the keypoints and descriptors with SIFT
    key_points, descriptions = sift.detectAndCompute(get_lines_from_image(image), None)
    return ImageSiftResult(key_points, descriptions)


def get_lines_from_image(image: ImageCv2):
    line_image = np.copy(image) * 0  # creating a blank to draw lines on
    lines = lsd(image, scale=0.5, eps=50, n_bins=100)

    for line in lines:
        x1, y1, x2, y2 = (int(line[0]), int(line[1]), int(line[2]), int(line[3]))
        cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
    im_blur = cv2.GaussianBlur(line_image, (7, 7), 0)
    return im_blur


