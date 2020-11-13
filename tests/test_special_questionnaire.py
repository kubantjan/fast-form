import os
import unittest

from config.configuration_loading import get_processing_config
from process_to_validation_excel import process_document_to_excel, load_paths_for_processing_config


class TestWholeProcess(unittest.TestCase):
    document_path = "form2_for_test/document.jpg"
    config_path = "form2_for_test/path_config.json"
    excel_path = "form2_for_test/result.xlsx"
    paths_for_processing_config = load_paths_for_processing_config(config_path)
    processing_config = get_processing_config(paths_for_processing_config)

    def test_process_to_excel(self):
        if os.path.exists(self.excel_path):
            os.remove(self.excel_path)
        process_document_to_excel(document_path=self.document_path,
                                  processing_config=self.processing_config,
                                  excel_path=self.excel_path)
