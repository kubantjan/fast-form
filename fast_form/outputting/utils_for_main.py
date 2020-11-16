import json
import logging
import os

import dacite
import pandas as pd
from openpyxl import load_workbook

from fast_form.config.configuration_dataclasses import PathsForProcessingConfig
from fast_form.config.configuration_loading import get_processing_config
from fast_form.outputting.process_document import process_document_and_add_to_validation_excel

SHEET_WITH_RESULTS = "automatic_results"
VALIDATION_EXCEL_NAME = "validation_excel.xlsx"

logger = logging.getLogger(__name__)


def process_to_validation_excel(paths_for_processing_config: PathsForProcessingConfig):
    processing_config = get_processing_config(paths_for_processing_config)
    validation_excel_path = os.path.join(paths_for_processing_config.folder_with_documents_path, VALIDATION_EXCEL_NAME)
    if os.path.exists(validation_excel_path):
        os.remove(validation_excel_path)

    document_names = [file for file in os.listdir(paths_for_processing_config.folder_with_documents_path) if
                      file.endswith('.pdf') or file.endswith(".jpg") or file.endswith(".png")]
    logging.info(f"Processing to validation excel from {paths_for_processing_config.folder_with_documents_path}. Number"
                 f" of documents is {len(document_names)}")
    for document_name in document_names:
        process_document_and_add_to_validation_excel(
            os.path.join(paths_for_processing_config.folder_with_documents_path, document_name),
            processing_config,
            validation_excel_path
        )
    logger.info(
        f"Successfully processed all documents from '{paths_for_processing_config.folder_with_documents_path}' to "
        f"validation excel '{validation_excel_path}'")


def process_to_final_excel(paths_for_processing_config: PathsForProcessingConfig):
    validation_excel_path = os.path.join(paths_for_processing_config.folder_with_documents_path,
                                         VALIDATION_EXCEL_NAME)
    if not os.path.exists(validation_excel_path):
        raise FileNotFoundError(f"Validation excel with path '{validation_excel_path}' must exist")

    validation_df = pd.read_excel(validation_excel_path)
    one_patient_per_row_df = (
        validation_df
            .set_index(['patient_id', 'name'])
            .data
            .apply(lambda response_or_error: response_or_error if response_or_error >= 0 else "")
            .unstack(level=1)
    )

    combined_one_patient_per_row_df = one_patient_per_row_df

    if os.path.exists(paths_for_processing_config.final_excel_path):
        xl = pd.ExcelFile(paths_for_processing_config.final_excel_path)
        if SHEET_WITH_RESULTS in xl.sheet_names:  # see all sheet names
            old_one_patient_per_row_df = xl.parse(
                index_col="patient_id",
                keep_default_na=False,
                na_values=[],
                sheet_name=SHEET_WITH_RESULTS)

            combined_one_patient_per_row_df = one_patient_per_row_df.combine_first(old_one_patient_per_row_df)

    book = load_workbook(paths_for_processing_config.final_excel_path)
    writer = pd.ExcelWriter(paths_for_processing_config.final_excel_path, engine='openpyxl')
    if SHEET_WITH_RESULTS in book.sheetnames:
        book.remove(book[SHEET_WITH_RESULTS])
    writer.book = book
    combined_one_patient_per_row_df.to_excel(writer, sheet_name=SHEET_WITH_RESULTS)
    writer.save()
    logger.info(f"Successfully processed from validation excel: '{validation_excel_path}'"
                f" to final excel '{paths_for_processing_config.final_excel_path}'")


def load_paths_for_processing_config(path_configuration: str) -> PathsForProcessingConfig:
    def join(rel_path):
        return os.path.join(os.path.dirname(path_configuration), rel_path)

    with open(path_configuration, "rb") as f:
        relative_paths = dacite.from_dict(data_class=PathsForProcessingConfig, data=json.loads(f.read()))
    return PathsForProcessingConfig(
        template_path=join(relative_paths.template_path),
        folder_with_documents_path=join(relative_paths.folder_with_documents_path),
        final_excel_path=join(relative_paths.final_excel_path),
        form_structure_path=join(relative_paths.form_structure_path)
    )
