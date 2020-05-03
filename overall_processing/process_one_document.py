import json

import cv2

from field_recognizer.recognize_all import recognize
from preprocessing.preprocess import preprocess
from structure_parser.formstructureparser import FormStructureParser


def process_document(im, config):
    fsp = FormStructureParser(config)

    im = preprocess(im, config)
    form_data = fsp.process_form(im)
    form_data = recognize(form_data)

    return form_data


if __name__ == '__main__':
    image_path = "test/example_forms/julinka_dotaznik/front_page.jpg"
    with open("test/example_forms/julinka_dotaznik/front_page_config.json", 'r') as f:
        config = json.load(f)
    im = cv2.imread(image_path)

    form_data = process_document(im, config)
