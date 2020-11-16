import cv2

from fast_form.config.configuration_dataclasses import ImageCv2, ImageSiftResult


def get_image_sift_result(image: ImageCv2) -> ImageSiftResult:
    sift = cv2.SIFT_create()
    # find the keypoints and descriptors with SIFT
    key_points, descriptions = sift.detectAndCompute(image, None)
    return ImageSiftResult(key_points, descriptions)
