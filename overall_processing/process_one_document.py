import json

import cv2
import numpy as np
import pandas as pd
import os

from field_recognizer.recognize_all import recognize
from preprocessing.preprocess import preprocess
from structure_parser.formstructureparser import FormStructureParser


def process_document(im, config):
    fsp = FormStructureParser(config)

    im = preprocess(im, config)
    form_data = fsp.process_form(im)
    form_data = recognize(form_data)

    return form_data


def output_data(form_data, name):
    d = dict()
    fil = form_data["fields"]
    for field in fil:
        if field["type"] == "boxes":
            data = np.argmax(field["recognized"])
        elif field["type"] == "letters":
            data = "".join(field["recognized"])

        field_name = field["name"] + field["type"]
        d[f'{field_name}_data'] = data,
        d[f'{field_name}_acc'] = min(field["accuracy"])
        d[f'{field_name}_img'] = f"{field_name}_img.png"
        cv2.imwrite(os.path.join(os.path.dirname(name), f"{field_name}_img.png"), field["img"])

    df = pd.DataFrame(d)
    filename = f"{name.split('.')[0]}.xlsx"
    df.to_excel(filename, index=False)
    return filename


if __name__ == '__main__':
    image_path = "test/example_forms/julinka_dotaznik/front_page.jpg"
    with open("test/example_forms/julinka_dotaznik/front_page_config.json", 'r') as f:
        config = json.load(f)
    im = cv2.imread(image_path)

    form_data = process_document(im, config)
    filename = output_data(form_data, image_path)
