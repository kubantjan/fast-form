import os
import unittest

import pandas as pd

from fast_form.config.configuration_loading import get_processing_config
from fast_form.outputting.ouput_data import output_data
from fast_form.outputting.process_document import process_document, process_document_and_add_to_validation_excel
from fast_form.outputting.utils_for_main import load_paths_for_processing_config, VALIDATION_EXCEL_NAME


class TestWholeProcess(unittest.TestCase):
    path_config_path = os.path.normpath(os.path.join(os.path.dirname(__file__),
                                                     os.path.normpath("form1_for_test/path_config.json")))
    paths_for_processing_config = load_paths_for_processing_config(path_config_path)
    document_path = os.path.join(paths_for_processing_config.folder_with_documents_path, "document.jpg")
    processing_config = get_processing_config(paths_for_processing_config)

    def test_letters_numbers_boxes_recognized_output_created(self):
        form_data = process_document(document_path=self.document_path, processing_config=self.processing_config)
        exp = pd.DataFrame(
            index=[0, 1, 2, 3],
            data={
                "name": ["Spali jste během Unihacku?", "Datum vyplnění", "Jméno týmu", "Chcete přepis, nebo zmrzlinu?"],
                "data": [3, "03 05 2020", "RYCHLY MQUCHY", 1]
            })

        df, images = output_data(form_data, "test_patient_id")
        pd.testing.assert_frame_equal(exp, df[["name", "data"]])

    def test_process_to_excel(self):
        validation_excel_path = os.path.join(self.paths_for_processing_config.folder_with_documents_path,
                                             VALIDATION_EXCEL_NAME)
        if os.path.exists(validation_excel_path):
            os.remove(validation_excel_path)
        process_document_and_add_to_validation_excel(document_path=self.document_path,
                                                     processing_config=self.processing_config,
                                                     excel_path=validation_excel_path)
        process_document_and_add_to_validation_excel(document_path=self.document_path,
                                                     processing_config=self.processing_config,
                                                     excel_path=validation_excel_path)
