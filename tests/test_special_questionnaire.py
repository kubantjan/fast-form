import os
import unittest

from config.configuration_loading import get_processing_config
from outputting.process_document import process_document_and_add_to_validation_excel
from outputting.utils_for_main import load_paths_for_processing_config


class TestWholeProcess(unittest.TestCase):
    document_path = "tests/form2_for_test/document.jpg"
    config_path = "tests/form2_for_test/path_config.json"
    excel_path = "tests/form2_for_test/result.xlsx"
    paths_for_processing_config = load_paths_for_processing_config(config_path)
    processing_config = get_processing_config(paths_for_processing_config)

    def test_process_to_excel(self):
        if os.path.exists(self.excel_path):
            os.remove(self.excel_path)
        process_document_and_add_to_validation_excel(document_path=self.document_path,
                                                     processing_config=self.processing_config,
                                                     excel_path=self.excel_path)
