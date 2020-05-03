import json

import cv2

from field_recognizer.recognize_all import recognize
from preprocessing.preprocess import preprocess
from structure_parser.formstructureparser import FormStructureParser
from field_reccongnizer.model import load_model, load_result_mapper


def process_document(im, config, model, result_mapper):
    fsp = FormStructureParser(config)

    im = preprocess(im, config)
    form_data = fsp.process_form(im)
    form_data = recognize(form_data, model, result_mapper)

    return form_data


if __name__ == '__main__':
    # define paths
    image_path = "test/example_forms/julinka_dotaznik/front_page.jpg"
    model_structure_path = "model_data/model.json"
    model_weights_path = "model_data/model.h5"
    result_mapper_path = "training_data/emnist-balanced-mapping.txt"

    # load model
    model = load_model(model_structure_path, model_weights_path)

    # load result mapper
    result_mapper = load_result_mapper(result_mapper_path)

    # open config
    with open("test/example_forms/julinka_dotaznik/front_page_config.json", 'r') as f:
        config = json.load(f)
    im = cv2.imread(image_path)

    # process
    form_data = process_document(im, config, model, result_mapper)
