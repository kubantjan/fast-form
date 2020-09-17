import cv2
import numpy as np

from config.configuration import ImageSiftResult, Template


def normalize(img: np.ndarray) -> np.ndarray:
    """Converts `im` to black and white.

    Applying a threshold to a grayscale image will make every pixel either
    fully black or fully white."""

    im_blur = cv2.GaussianBlur(img, (7, 7), 0)

    im_gray = cv2.cvtColor(im_blur, cv2.COLOR_BGR2GRAY)
    im_thresh = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return im_thresh


def get_image_sift_result(image: np.ndarray) -> ImageSiftResult:
    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    key_points, descriptions = sift.detectAndCompute(image, None)
    return ImageSiftResult(key_points, descriptions)


def create_template(template_image_path: str) -> Template:
    image = cv2.imread(template_image_path)
    sift_result = get_image_sift_result(image)
    return Template(sift_result, image)


def fit_image_to_template(image: np.ndarray, template: Template):
    # based on https://towardsdatascience.com/image-stitching-using-opencv-817779c86a83
    sift_result = get_image_sift_result(image)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(sift_result.descriptions, template.sift_result.descriptions, k=2)

    # Apply ratio test
    good_matches = []
    for match in matches:
        if match[0].distance < 0.5 * match[1].distance:
            good_matches.append(match)
    good_matches = np.asarray(good_matches)

    if len(good_matches[:, 0]) >= 4:
        image_similarities = np.float32(
            [sift_result.key_points[match.queryIdx].pt for match in good_matches[:, 0]]
        ).reshape(-1, 1, 2)
        template_similarities = np.float32(
            [template.sift_result.key_points[match.trainIdx].pt for match in good_matches[:, 0]]).reshape(-1, 1, 2)
        homography_matrix, _ = cv2.findHomography(image_similarities, template_similarities, cv2.RANSAC, 5.0)

        return cv2.warpPerspective(image, homography_matrix, (template.image.shape[1], template.image.shape[0]))
    else:
        raise AssertionError("Cant find enough keypoints.")


def preprocess(im, template: Template) -> np.ndarray:
    """Runs the full pipeline:

    - Loads input image
    - Normalizes image
    - fits to original
    """
    normalized_image = normalize(im)

    fitted_image = fit_image_to_template(normalized_image, template=template)

    return fitted_image
