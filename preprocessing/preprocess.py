import cv2
import numpy as np
import pandas as pd


def normalize(img, show_borders=False):
    """Converts `im` to black and white.

    Applying a threshold to a grayscale image will make every pixel either
    fully black or fully white."""

    im_blur = cv2.GaussianBlur(img, (5, 5), 0)
    # im_blur = cv2.medianBlur(img,5) # does not wokr that well

    im_gray = cv2.cvtColor(im_blur, cv2.COLOR_BGR2GRAY)
    if show_borders:
        thresh = 240
    else:
        thresh = 160
    return cv2.threshold(
        im_gray, thresh, 255, type=0)[1]


def is_approx_corner(x):
    rect = cv2.boundingRect(x)
    side_ratio = rect[2]/rect[3]
    return (side_ratio > 0.5) and (side_ratio < 2)


def get_corners(im):
    cont, hie = cv2.findContours(255 - im, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return (
        pd.DataFrame([cont, hie[0]])
            .T
            .assign(size=lambda df: df[0].apply(cv2.contourArea))
            .sort_values(by="size", ascending=False)
            .loc[lambda df: df[1].apply(lambda x: (x[2] == -1) & (x[3] == -1))]
            .loc[lambda df: df[0].apply(is_approx_corner)]
            .iloc[0:4]
            [0]
            .values
    )


def get_bounding_rect(contour):
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    return np.int0(box)


def features_distance(f1, f2):
    return np.linalg.norm(np.array(f1) - np.array(f2))


def sort_points_counter_clockwise(points):
    origin = np.mean(points, axis=0)

    def positive_angle(p):
        x, y = p - origin
        ang = np.arctan2(y, x)
        return 2 * np.pi + ang if ang < 0 else ang

    return sorted(points, key=positive_angle)


def get_outmost_points(contours):
    all_points = np.concatenate(contours)
    return get_bounding_rect(all_points)


def crop_to_corners(im, outmost):
    x_max = max([x[0] for x in outmost])
    x_min = min([x[0] for x in outmost])
    y_max = max([x[1] for x in outmost])
    y_min = min([x[1] for x in outmost])

    return im[y_min:y_max, x_min:x_max]


def preprocess(im, config, show_borders=False) -> np.ndarray:
    """Runs the full pipeline:

    - Loads input image
    - Normalizes image
    - Finds contours
    - Finds corners among all contours
    - Finds 'outmost' points of all corners
    - Applies perpsective transform to get a bird's eye view
    - Scans each line for the marked alternative
    """

    im = normalize(im, show_borders)

    corners = get_corners(im)

    outmost = sort_points_counter_clockwise(get_outmost_points(corners))

    im = crop_to_corners(im, outmost)

    im = cv2.resize(im, (config["width"], config["height"]))

    return im
