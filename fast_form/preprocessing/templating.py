import logging
from typing import List

from fast_form.config.configuration_dataclasses import Template, ImageCv2
from fast_form.preprocessing.image_sift import get_image_sift_result
from fast_form.preprocessing.normalization import normalize
from fast_form.utils.image_loading import load_images_from_path

PDF_TEMPLATE = "template.pdf"
PICKLE_TEMPLATE = "template.pickle"
IMAGE_TEMPLATE = "template.png"
IMAGE_TEMPLATE_2 = "template.jpg"

logger = logging.getLogger(__name__)


def get_template_from_normalized_image(image: ImageCv2) -> Template:
    sift_result = get_image_sift_result(image)
    return Template(sift_result, image)


def get_templates(template_image_path: str) -> List[Template]:
    logger.info("Calculating properties of templates, can tak a long time")
    images = load_images_from_path(template_image_path)

    templates = [get_template_from_normalized_image(normalize(im)) for im in images]
    return templates
