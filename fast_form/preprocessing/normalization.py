import cv2
import numpy as np


def normalize(img: np.ndarray) -> np.ndarray:
    """Converts `im` to black and white.

    Applying a threshold to a grayscale image will make every pixel either
    fully black or fully white."""

    im_blur = cv2.GaussianBlur(img, (7, 7), 0)

    im_gray = cv2.cvtColor(im_blur, cv2.COLOR_BGR2GRAY)
    im_thresh = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return im_thresh
