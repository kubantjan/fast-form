import cv2
import numpy as np


def normalize(img):
    """Converts `im` to black and white.

    Applying a threshold to a grayscale image will make every pixel either
    fully black or fully white."""

    im_blur = cv2.GaussianBlur(img,(5,5),0)
    # im_blur = cv2.medianBlur(img,5) # does not wokr that well

    im_gray = cv2.cvtColor(im_blur, cv2.COLOR_BGR2GRAY)

    thresh = 160  # use 200 when you want to see boxes around letters for debugging
    return cv2.threshold(
        im_gray, thresh, 255, type=0)[1]


def get_approx_contour(contour, tol=.01):
    """Gets rid of 'useless' points in the contour."""
    epsilon = tol * cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, epsilon, True)


def get_contours(image_gray):
    contours, _ = cv2.findContours(
        image_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return map(get_approx_contour, contours)


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


def preprocess(im, config) -> np.ndarray:
    """Runs the full pipeline:

    - Loads input image
    - Normalizes image
    - Finds contours
    - Finds corners among all contours
    - Finds 'outmost' points of all corners
    - Applies perpsective transform to get a bird's eye view
    - Scans each line for the marked alternative
    """

    im = normalize(im)

    contours = get_contours(im)

    corners = sorted(contours, key=lambda x: - cv2.contourArea(x))[1:5]

    outmost = sort_points_counter_clockwise(get_outmost_points(corners))

    im = crop_to_corners(im, outmost)

    im = cv2.resize(im, (config["width"], config["height"]))

    return im
