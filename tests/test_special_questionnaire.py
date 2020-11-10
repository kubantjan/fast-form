import os
import unittest

from main import process_document_to_excel, load_processing_config


class TestWholeProcess(unittest.TestCase):
    document_path = "form2_for_test/document.jpg"
    config_path = "form2_for_test/path_config.json"
    excel_path = "form2_for_test/result.xlsx"
    processing_config = load_processing_config(config_path)

    def test_process_to_excel(self):
        if os.path.exists(self.excel_path):
            os.remove(self.excel_path)
        process_document_to_excel(document_path=self.document_path,
                                  processing_config=self.processing_config,
                                  excel_path=self.excel_path)
