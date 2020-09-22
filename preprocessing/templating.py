import cv2
import numpy as np
from PIL.PpmImagePlugin import PpmImageFile
from pdf2image import convert_from_path

from config.configuration import ImageCv2, Template, FormTemplates
from preprocessing.image_sift import get_image_sift_result
from preprocessing.normalization import normalize

PDF_TEMPLATE = "template.pdf"
PICKLE_TEMPLATE = "template.pickle"
IMAGE_TEMPLATE = "template.png"
IMAGE_TEMPLATE_2 = "template.jpg"


def get_template_from_image(image: ImageCv2) -> Template:
    sift_result = get_image_sift_result(image)
    return Template(sift_result, image)


def to_cv_image(pid_image: PpmImageFile) -> ImageCv2:
    return normalize(np.array(pid_image.convert('RGB')))


def get_templates(template_image_path: str) -> FormTemplates:
    ending = template_image_path.lower().split(".")[-1]
    if ending == "pdf":
        images = [to_cv_image(im_pip) for im_pip in
                  convert_from_path(template_image_path, dpi=300)]
    elif ending in {"jpg", "png", "jpeg"}:
        images = [cv2.imread(template_image_path)]
    else:
        raise ValueError(f"Uknown file format file: {template_image_path}")
    templates = [get_template_from_image(im) for im in images]
    return FormTemplates(templates)
