import argparse
import json
import os

import cv2
import numpy as np
import pandas as pd

from field_recognizer.model import load_model
from field_recognizer.recognize_all import recognize
from preprocessing.preprocess import preprocess
from structure_parser.formstructureparser import FormStructureParser


def process_document(im, config, model_letters, model_numbers, letter_mapper, number_mapper):
    fsp = FormStructureParser(config)

    im = preprocess(im, config)
    form_data = fsp.process_form(im)
    form_data = recognize(form_data, model_letters, model_numbers, letter_mapper, number_mapper)

    return form_data


def output_data(form_data, name):
    d = dict()
    fil = form_data["fields"]
    for field in fil:
        if field["type"] == "boxes":
            data = field["answers"][np.argmax(field["recognized"])]
        elif field["type"] == "letters":
            data = "".join(field["recognized"])
        elif field["type"] == "numbers":
            data = "".join(field["recognized"])

        field_name = field["name"]
        d[f'{field_name}_data'] = data,
        d[f'{field_name}_acc'] = min(field["accuracy"])
        d[f'{field_name}_img'] = f"{field_name}_img.png"
        cv2.imwrite(os.path.join(os.path.dirname(name), f"{field_name}_img.png"), field["img"])

    df = pd.DataFrame(d)
    filename = f"{name.split('.')[0]}.xlsx"
    df.to_excel(filename, index=False)
    return filename


def load_config(config_path):
    with open(config_path, "rb") as f:
        return json.loads(f.read())


if __name__ == '__main__':
    # parse CLI args
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", '-c', help="Pass config file.")
    args = parser.parse_args()

    # define paths
    config = load_config(args.config)

    image_path = config["image_path"]
    model_letters_structure_path = config["model_letters_structure_path"]
    model_letters_weights_path = config["model_letters_weights_path"]
    model_numbers_structure_path = config["model_numbers_structure_path"]
    model_numbers_weights_path = config["model_numbers_weights_path"]

    letter_mapper_path = config["letter_mapper_path"]
    number_mapper_path = config["number_mapper_path"]

    image_config_path = config["image_config_path"]

    # load model
    model_letters = load_model(model_letters_structure_path, model_letters_weights_path)
    model_numbers = load_model(model_numbers_structure_path, model_numbers_weights_path)

    # load result mapper

    with open(letter_mapper_path, "r") as json_file:
        letter_mapper = json.load(json_file)
        letter_mapper = {int(k): v for k, v in letter_mapper.items()}

    with open(number_mapper_path, "r") as json_file:
        number_mapper = json.load(json_file)
        number_mapper = {int(k): v for k, v in number_mapper.items()}

    # open config
    with open(image_config_path, 'r') as f:
        config = json.load(f)
    im = cv2.imread(image_path)

    # process
    form_data = process_document(im, config, model_letters, model_numbers, letter_mapper, number_mapper)
    filename = output_data(form_data, image_path)
