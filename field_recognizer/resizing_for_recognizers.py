import math

import cv2
import numpy as np


def resize(img: np.ndarray, full_dimension: int, border: int):
    w, h = img.shape
    maxi = max([w, h])
    if maxi == 0:
        return np.array([])

    dimension = full_dimension - (border * 2)
    r = dimension / maxi
    new_w = round(w * r)
    new_h = round(h * r)

    res = cv2.resize(img, dsize=(new_h, new_w), interpolation=cv2.INTER_CUBIC)
    if max(res.shape) != dimension:
        raise ValueError(f"not good size of resized shape: {res.shape}, fix! ")

    bottom = math.ceil((dimension - new_w) / 2) + border
    top = math.floor((dimension - new_w) / 2) + border
    right = math.ceil((dimension - new_h) / 2) + border
    left = math.floor((dimension - new_h) / 2) + border
    res = cv2.copyMakeBorder(res, top, bottom, left, right, cv2.BORDER_CONSTANT, value=255)

    return res
