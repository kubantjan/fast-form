import json
import logging
import os

import dacite

from config.configuration_dataclasses import PathsForProcessingConfig, ProcessingConfig
from config.configuration_loading import get_processing_config
from outputting.process_document import process_document_to_excel

PATH_TO_PATH_CONFIG = "../scany/path_config.json"

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def load_processing_config(path_configuration) -> ProcessingConfig:
    with open(path_configuration, "rb") as f:
        paths_for_processing_config = dacite.from_dict(data_class=PathsForProcessingConfig, data=json.loads(f.read()))
    return get_processing_config(paths_for_processing_config)


if __name__ == '__main__':
    processing_config = load_processing_config(PATH_TO_PATH_CONFIG)
    excel_path = os.path.join(processing_config.folder_with_documents_path, "result.xlsx")
    if os.path.exists(excel_path):
        os.remove(excel_path)

    for document_name in os.listdir(processing_config.folder_with_documents_path):
        if document_name.endswith(".pdf"):
            process_document_to_excel(
                os.path.join(processing_config.folder_with_documents_path, document_name),
                processing_config,
                excel_path
            )
