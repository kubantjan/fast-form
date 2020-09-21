import cv2

from config.configuration import ImageCv2, ImageSiftResult


def get_image_sift_result(image: ImageCv2) -> ImageSiftResult:
    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    key_points, descriptions = sift.detectAndCompute(image, None)
    return ImageSiftResult(key_points, descriptions)
