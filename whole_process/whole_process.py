import json

import cv2
import dacite

from config.configuration import PathConfig, Models
from field_recognizer.model import load_model
from field_recognizer.recognize_all import recognize
from preprocessing.preprocess import preprocess, create_template
from structure_parser.form_structure_parser import FormStructureParser


def load_path_config(config_path) -> PathConfig:
    with open(config_path, "rb") as f:
        return dacite.from_dict(data_class=PathConfig, data=json.loads(f.read()))


def load_models(model_data_location: str):
    model_letters_structure_path = f"{model_data_location}/model_letters.json"
    model_letters_weights_path = f"{model_data_location}/model_letters.h5"
    model_numbers_structure_path = f"{model_data_location}/model_numbers.json"
    model_numbers_weights_path = f"{model_data_location}/model_numbers.h5"
    letter_mapper_path = f"{model_data_location}/model_letters_mapping.json"
    number_mapper_path = f"{model_data_location}/model_numbers_mapping.json"

    model_letters = load_model(model_letters_structure_path, model_letters_weights_path)
    model_numbers = load_model(model_numbers_structure_path, model_numbers_weights_path)

    # load result mapper

    with open(letter_mapper_path, "r") as json_file:
        letter_mapper = json.load(json_file)
        letter_mapper = {int(k): v for k, v in letter_mapper.items()}

    with open(number_mapper_path, "r") as json_file:
        number_mapper = json.load(json_file)
        number_mapper = {int(k): v for k, v in number_mapper.items()}

    return Models(model_letters=model_letters, model_numbers=model_numbers, letter_mapper=letter_mapper,
                  number_mapper=number_mapper)


def process_image(path_to_path_config: str, image_path: str):
    path_config = load_path_config(path_to_path_config)
    with open(path_config.form_structure_config_path, 'r') as f:
        form_structure_parser = FormStructureParser(json.load(f))
    models = load_models(path_config.model_data_location)
    template = create_template(path_config.template_image_path)

    image = cv2.imread(image_path)
    image = preprocess(image, template)
    form_data = form_structure_parser.process_form(image)
    form_data = recognize(form_data, models)

    return form_data
