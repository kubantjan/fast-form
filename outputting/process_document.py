import json

import dacite
from dacite import Config

from config.configuration import PathConfig, Models
from field_recognizer.model import load_model
from field_recognizer.recognize_all import recognize
from preprocessing.preprocess import preprocess
from preprocessing.templating import get_templates
from structure_parser.form_structure_dataclasses import FieldType, Orientation, FormData
from structure_parser.page_structure_parser import PageStructureParser
from utils.image_loading import load_images_from_path

LETTERS_MODEL_JSON = "model_letters.json"
LETTERS_MODEL_H5 = "model_letters.h5"
NUMBERS_MODEL_JSON = "model_numbers.json"
NUMBERS_MODEL_H5 = "model_numbers.h5"
LETTER_MAPPER_JSON = "model_letters_mapping.json"
NUMBER_MAPPER_JSON = "model_numbers_mapping.json"


def load_path_configuration(path_configuration) -> PathConfig:
    with open(path_configuration, "rb") as f:
        return dacite.from_dict(data_class=PathConfig, data=json.loads(f.read()))


def load_models(model_data_location: str):
    model_letters_structure_path = f"{model_data_location}/{LETTERS_MODEL_JSON}"
    model_letters_weights_path = f"{model_data_location}/{LETTERS_MODEL_H5}"
    model_numbers_structure_path = f"{model_data_location}/{NUMBERS_MODEL_JSON}"
    model_numbers_weights_path = f"{model_data_location}/{NUMBERS_MODEL_H5}"
    letter_mapper_path = f"{model_data_location}/{LETTER_MAPPER_JSON}"
    number_mapper_path = f"{model_data_location}/{NUMBER_MAPPER_JSON}"

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


def load_form_structure(form_structure_config_path: str) -> FormData:
    with open(form_structure_config_path, 'r') as f:
        return dacite.from_dict(data_class=FormData, data=json.load(f),
                                config=Config(cast=[FieldType, Orientation]))


def process_document(path_to_path_config: str, document_path: str) -> FormData:
    path_config = load_path_configuration(path_to_path_config)

    models = load_models(path_config.model_data_location)
    templates = get_templates(path_config.template_image_path)
    images = load_images_from_path(document_path)
    form_structure = load_form_structure(path_config.form_structure_config_path)

    assert len(templates) == form_structure.page_count
    assert len(images) == form_structure.page_count

    for image, template, (page_name, page_structure) in zip(images, templates, form_structure.form_page_data.items()):
        image = preprocess(image, [template])
        page_structure_parser = PageStructureParser(page_structure)
        page_data = page_structure_parser.process_page(image)
        page_data = recognize(page_data, models)
        form_structure.form_page_data[page_name] = page_data

    return form_structure
