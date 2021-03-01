import os
import unittest

from fast_form.config.configuration_loading import get_processing_config
from fast_form.outputting.process_document import process_document_and_add_to_validation_excel
from fast_form.outputting.utils_for_main import load_paths_for_processing_config, process_to_final_excel


class TestWholeProcess(unittest.TestCase):
    path_config_path = os.path.normpath(os.path.join(os.path.dirname(__file__),
                                                     os.path.normpath("form2_for_test/path_config.json")))
    paths_for_processing_config = load_paths_for_processing_config(path_config_path)
    document_path = os.path.join(paths_for_processing_config.folder_with_documents_path, "document.jpg")
    processing_config = get_processing_config(paths_for_processing_config)

    def test_process_to_excel(self):
        if os.path.exists(self.paths_for_processing_config.validation_excel_path):
            os.remove(self.paths_for_processing_config.validation_excel_path)
        process_document_and_add_to_validation_excel(document_path=self.document_path,
                                                     processing_config=self.processing_config,
                                                     excel_path=self.paths_for_processing_config.validation_excel_path)
        process_to_final_excel(self.paths_for_processing_config)
