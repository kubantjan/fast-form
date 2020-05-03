import cv2
import numpy as np

from configuration.const import CORNER_IMG_PATH


def calculate_contour_features(contour):
    """Calculates interesting properties (features) of a contour.

    We use these features to match shapes (contours). In this script,
    we are interested in finding shapes in our input image that look like
    a corner. We do that by calculating the features for many contours
    in the input image and comparing these to the features of the corner
    contour. By design, we know exactly what the features of the real corner
    contour look like - check out the calculate_corner_features function.

    It is crucial for these features to be invariant both to scale and rotation.
    In other words, we know that a corner is a corner regardless of its size
    or rotation. In the past, this script implemented its own features, but
    OpenCV offers much more robust scale and rotational invariant features
    out of the box - the Hu moments.
    """
    moments = cv2.moments(contour)
    return cv2.HuMoments(moments)


def calculate_corner_features(corner_path='images/corners/corner.png'):
    """Calculates the array of features for the corner contour.
    In practice, this can be pre-calculated, as the corners are constant
    and independent from the inputs.

    We load the img/corner.png file, which contains a single corner, so we
    can reliably extract its features. We will use these features to look for
    contours in our input image that look like a corner.
    """
    corner_img = cv2.imread(corner_path)
    corner_img_gray = cv2.cvtColor(corner_img, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(
        corner_img_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # We expect to see only two contours:
    # - The "outer" contour, which wraps the whole image, at hierarchy level 0
    # - The corner contour, which we are looking for, at hierarchy level 1
    # If in trouble, one way to check what's happening is to draw the found contours
    # with cv2.drawContours(CORNER_IMG_PATH, contours, -1, (255, 0, 0)) and try and find
    # the correct corner contour by drawing one contour at a time. Ideally, this
    # would not be done at runtime.
    if len(contours) != 2:
        raise RuntimeError(
            'Did not find the expected contours when looking for the corner')

    # Following our assumptions as stated above, we take the contour that has a parent
    # contour (that is, it is _not_ the outer contour) to be the corner contour.
    # If in trouble, verify that this contour is the corner contour with
    # cv2.drawContours(CORNER_IMG_PATH, [corner_contour], -1, (255, 0, 0))
    corner_contour = next(ct
                          for i, ct in enumerate(contours)
                          if hierarchy[0][i][3] != -1)

    return calculate_contour_features(corner_contour)


def normalize(im):
    """Converts `im` to black and white.

    Applying a threshold to a grayscale image will make every pixel either
    fully black or fully white. Before doing so, a common technique is to
    get rid of noise (or super high frequency color change) by blurring the
    grayscale image with a Gaussian filter."""
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # Filter the grayscale image with a 3x3 kernel
    # blurred = cv2.GaussianBlur(im_gray, (3, 3), 0)

    # Applies a Gaussian adaptive thresholding. In practice, adaptive thresholding
    # seems to work better than appling a single, global threshold to the image.
    # This is particularly important if there could be shadows or non-uniform
    # lighting on the answer sheet. In those scenarios, using a global thresholding
    # technique might yield paricularly bad results.
    # The choice of the parameters blockSize = 77 and C = 10 is as much as an art
    # as a science and domain-dependand.
    # In practice, you might want to try different  values for your specific answer
    # sheet.

    # HERE ONE CAN SET thresh to 200 to see boxes when debugging
    return cv2.threshold(
        im_gray, 125, 255, type=0)[1]


def get_approx_contour(contour, tol=.01):
    """Gets rid of 'useless' points in the contour."""
    epsilon = tol * cv2.arcLength(contour, True)
    return cv2.approxPolyDP(contour, epsilon, True)


def get_contours(image_gray):
    contours, _ = cv2.findContours(
        image_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return map(get_approx_contour, contours)


def get_corners(contours):
    """Returns the 4 contours that look like a corner the most.

    In the real world, we cannot assume that the corners will always be present,
    and we likely need to decide how good is good enough for contour to
    look like a corner.
    This is essentially a classification problem. A good approach would be
    to train a statistical classifier model and apply it here. In our little
    exercise, we assume the corners are necessarily there."""
    corner_features = calculate_corner_features(corner_path=CORNER_IMG_PATH)
    return sorted(
        contours,
        key=lambda c: features_distance(
            corner_features,
            calculate_contour_features(c)))[:4]


def get_bounding_rect(contour):
    rect = cv2.minAreaRect(contour)
    box = cv2.boxPoints(rect)
    return np.int0(box)


def features_distance(f1, f2):
    return np.linalg.norm(np.array(f1) - np.array(f2))


def draw_point(point, img, radius=5, color=(0, 0, 255)):
    cv2.circle(img, tuple(point), radius, color, -1)


def get_centroid(contour):
    m = cv2.moments(contour)
    x = int(m["m10"] / m["m00"])
    y = int(m["m01"] / m["m00"])
    return (x, y)


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


def preprocess(source_file, config) -> np.ndarray:
    """Runs the full pipeline:

    - Loads input image
    - Normalizes image
    - Finds contours
    - Finds corners among all contours
    - Finds 'outmost' points of all corners
    - Applies perpsective transform to get a bird's eye view
    - Scans each line for the marked alternative
    """
    im = cv2.imread(source_file)

    im = normalize(im)

    contours = get_contours(im)

    corners = sorted(contours, key=lambda x: - cv2.contourArea(x))[1:5]

    outmost = sort_points_counter_clockwise(get_outmost_points(corners))

    im = crop_to_corners(im, outmost)

    im = cv2.resize(im, (config["width"], config["height"]))

    return im
