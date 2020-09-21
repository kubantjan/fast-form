from typing import List, Tuple

import cv2
import numpy as np

from config.configuration import ImageCv2, FormTemplates, ImageSiftResult, Template
from preprocessing.image_sift import get_image_sift_result

ENOUGH_GOOD_MATCHES_FOR_FIT = 4
import logging

logger = logging.getLogger(__name__)


def normalize(img: np.ndarray) -> np.ndarray:
    """Converts `im` to black and white.

    Applying a threshold to a grayscale image will make every pixel either
    fully black or fully white."""

    im_blur = cv2.GaussianBlur(img, (7, 7), 0)

    im_gray = cv2.cvtColor(im_blur, cv2.COLOR_BGR2GRAY)
    im_thresh = cv2.adaptiveThreshold(im_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return im_thresh


def get_good_matches_for_template(image_sift: ImageSiftResult, template_sift: ImageSiftResult) -> List[cv2.DMatch]:
    # based on https://towardsdatascience.com/image-stitching-using-opencv-817779c86a83

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(image_sift.descriptions, template_sift.descriptions, k=2)

    # Apply ratio test
    good_matches = []
    for match in matches:
        if match[0].distance < 0.5 * match[1].distance:
            good_matches.append(match[0])
    return good_matches


def find_best_template_match(image_sift: ImageSiftResult,
                             templates: FormTemplates) -> Tuple[List[cv2.DMatch], Template, int]:
    all_good_matches = [(get_good_matches_for_template(image_sift, template.sift), template, i)
                        for i, template in enumerate(templates.templates)]
    return max(all_good_matches, key=lambda good_matches_template: len(good_matches_template[0]))


def fit_image_to_templates(image: ImageCv2, templates: FormTemplates) -> Tuple[ImageCv2, int]:
    image_sift = get_image_sift_result(image)
    good_matches, template, template_index = find_best_template_match(image_sift, templates)

    if len(good_matches) >= ENOUGH_GOOD_MATCHES_FOR_FIT:
        image_similarities = np.float32(
            [image_sift.key_points[match.queryIdx].pt for match in good_matches]
        ).reshape(-1, 1, 2)
        template_similarities = np.float32(
            [template.sift.key_points[match.trainIdx].pt for match in good_matches]).reshape(-1, 1, 2)
        homography_matrix, _ = cv2.findHomography(image_similarities, template_similarities, cv2.RANSAC, 5.0)

        return cv2.warpPerspective(image, homography_matrix,
                                   (template.image.shape[1], template.image.shape[0])), template_index
    else:
        raise AssertionError("Cant find enough keypoints.")


def preprocess(im, form_templates: FormTemplates) -> np.ndarray:
    """Runs the full pipeline:

    - Loads input image
    - Normalizes image
    - fits to original
    """
    normalized_image = normalize(im)

    fitted_image, template_index = fit_image_to_templates(normalized_image, templates=form_templates)
    logger.info(f"Best fit page was {template_index}")

    return fitted_image
