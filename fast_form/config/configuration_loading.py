import json
import os

import dacite
from dacite import Config

from fast_form.config.configuration_dataclasses import Models, PathsForProcessingConfig, ProcessingConfig
from fast_form.field_recognizer.model import load_model
from fast_form.preprocessing.templating import get_templates
from fast_form.structure_parser.form_structure_dataclasses import FormStructure, FieldType, Orientation

LETTERS_MODEL_JSON = "model_letters.json"
LETTERS_MODEL_H5 = "model_letters.h5"
NUMBERS_MODEL_JSON = "model_numbers.json"
NUMBERS_MODEL_H5 = "model_numbers.h5"
LETTER_MAPPER_JSON = "model_letters_mapping.json"
NUMBER_MAPPER_JSON = "model_numbers_mapping.json"


def load_models():
    model_data_location = os.path.join(os.path.dirname(__file__), "..", "model_data")
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


def load_form_structure(form_structure_config_path: str) -> FormStructure:
    with open(form_structure_config_path, 'r') as f:
        return dacite.from_dict(data_class=FormStructure, data=json.load(f),
                                config=Config(cast=[FieldType, Orientation]))


def get_processing_config(paths: PathsForProcessingConfig) -> ProcessingConfig:
    return ProcessingConfig(
        models=load_models(),
        templates=get_templates(paths.template_path),
        form_structure=load_form_structure(paths.form_structure_path),
    )
