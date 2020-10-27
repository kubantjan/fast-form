import os

from outputting.ouput_data import output_data, save_data
from outputting.process_document import process_document

CONFIG_PATH = "./real_forms/justyna_dotazniky/path_config.json"
DOCUMENT_FOLDER = "/home/honza/Documents/UniHack/scany"


def process_document_to_excel(document_path: str, config_path: str):
    if os.path.exists(document_path):
        form_data = process_document(config_path, document_path=document_path)
        df, images = output_data(form_data)
        save_data(df, images, document_path=document_path)
    else:
        raise FileExistsError("Document file not found")


if __name__ == '__main__':
    for document_name in os.listdir(DOCUMENT_FOLDER):
        if document_name.endswith(".pdf"):
            process_document_to_excel(os.path.join(DOCUMENT_FOLDER, document_name), CONFIG_PATH)
