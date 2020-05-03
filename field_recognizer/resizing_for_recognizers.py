import cv2
import math


def resize(img, dimension):
    w, h = img.shape
    maxi = max([w, h])

    r = dimension / maxi
    new_w = math.floor(w * r)
    new_h = math.floor(h * r)

    res = cv2.resize(img, dsize=(new_h, new_w), interpolation=cv2.INTER_CUBIC)
    if max(res.shape) != dimension:
        raise ValueError("not good size of resized shape, fix!")

    bottom = math.ceil((dimension - new_h) / 2)
    top = math.floor((dimension - new_h) / 2)
    right = math.ceil((dimension - new_w) / 2)
    left = math.floor((dimension - new_w) / 2)
    res = cv2.copyMakeBorder(res, top, bottom, left, right, cv2.BORDER_CONSTANT, value=255)

    return res
