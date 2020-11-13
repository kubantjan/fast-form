import os
import unittest

import pandas as pd

from config.configuration_loading import get_processing_config
from outputting.ouput_data import output_data
from outputting.process_document import process_document
from process_to_validation_excel import process_document_to_excel, load_paths_for_processing_config


class TestWholeProcess(unittest.TestCase):
    document_path = "form1_for_test/document.jpg"
    path_config_path = "form1_for_test/path_config.json"
    excel_path = "form1_for_test/result.xlsx"
    paths_for_processing_config = load_paths_for_processing_config(path_config_path)
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
        if os.path.exists(self.excel_path):
            os.remove(self.excel_path)
        process_document_to_excel(document_path=self.document_path,
                                  processing_config=self.processing_config,
                                  excel_path=self.excel_path)
        process_document_to_excel(document_path=self.document_path,
                                  processing_config=self.processing_config,
                                  excel_path=self.excel_path)
