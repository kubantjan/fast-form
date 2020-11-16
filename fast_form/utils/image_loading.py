from typing import List

import numpy as np
from PIL.PpmImagePlugin import PpmImageFile
from cv2 import cv2
from pdf2image import convert_from_path

from fast_form.config.configuration_dataclasses import ImageCv2


def to_cv_image(pid_image: PpmImageFile) -> ImageCv2:
    return np.array(pid_image.convert('RGB'))


def load_images_from_path(template_image_path: str) -> List[np.array]:
    ending = template_image_path.lower().split(".")[-1]

    if ending == "pdf":
        images = [to_cv_image(im_pip) for im_pip in
                  convert_from_path(template_image_path, dpi=300)]
    elif ending in {"jpg", "png", "jpeg"}:
        images = [cv2.imread(template_image_path)]
    else:
        raise ValueError(f"Uknown file format file: {template_image_path}")
    return images
