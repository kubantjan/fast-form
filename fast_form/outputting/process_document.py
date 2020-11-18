import logging
import os

from fast_form.config.configuration_dataclasses import ProcessingConfig
from fast_form.field_recognizer.recognize_all import recognize
from fast_form.outputting.ouput_data import output_data, save_data
from fast_form.preprocessing.preprocess import preprocess
from fast_form.structure_parser.form_structure_dataclasses import FormStructure
from fast_form.structure_parser.page_structure_parser import PageStructureParser
from fast_form.utils.image_loading import load_images_from_path

logger = logging.getLogger(__name__)


def process_document_and_add_to_validation_excel(document_path: str, processing_config: ProcessingConfig,
                                                 excel_path: str):
    if os.path.exists(document_path):
        maybe_patient_id = os.path.basename(document_path).split(".")[0]
        form_data = process_document(processing_config, document_path=document_path)
        df, images = output_data(form_data, maybe_patient_id=maybe_patient_id)

        save_data(df, images, excel_path=excel_path)
    else:
        raise FileExistsError("Document file not found")


def process_document(processing_config: ProcessingConfig,
                     document_path: str) -> FormStructure:
    images = load_images_from_path(document_path)

    assert len(processing_config.templates) == processing_config.form_structure.page_count
    assert len(images) == processing_config.form_structure.page_count, f"len images is {len(images)} and page count " \
                                                                       f"is " \
                                                                       f"{processing_config.form_structure.page_count}"

    for image, template, (page_name, page_structure) in zip(images,
                                                            processing_config.templates,
                                                            processing_config.form_structure.form_page_data.items()):
        logger.debug(f"Processing page {page_name}")
        image = preprocess(image, [template])
        page_structure_parser = PageStructureParser(page_structure)
        page_data = page_structure_parser.process_page(image)
        page_data = recognize(page_data, processing_config.models)
        processing_config.form_structure.form_page_data[page_name] = page_data

    return processing_config.form_structure
