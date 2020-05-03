import cv2
import math

EMNIST_SIZE = 28


def resize_letter(img):
    w, h = img.shape
    maxi = max([w, h])

    r = EMNIST_SIZE / maxi
    new_w = math.floor(w * r)
    new_h = math.floor(h * r)

    res = cv2.resize(img, dsize=(new_w, new_h), interpolation=cv2.INTER_CUBIC)
    if max(res.shape) != EMNIST_SIZE:
        raise ValueError("not good size of resized shape, fix!")

    bottom = math.ceil((EMNIST_SIZE - new_h) / 2)
    top = math.floor((EMNIST_SIZE - new_h) / 2)
    right = math.ceil((EMNIST_SIZE - new_w) / 2)
    left = math.floor((EMNIST_SIZE - new_w) / 2)
    res = cv2.copyMakeBorder(res, top, bottom, left, right, cv2.BORDER_CONSTANT, value=255)

    return res
