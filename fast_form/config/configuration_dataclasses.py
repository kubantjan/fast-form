from dataclasses import dataclass
from typing import List, Any, Dict

import cv2
import numpy as np

from fast_form.structure_parser.form_structure_dataclasses import FormStructure

ImageCv2 = np.ndarray


@dataclass
class ImageSiftResult:
    key_points: List[cv2.KeyPoint]
    descriptions: np.ndarray


@dataclass
class Template:
    sift: ImageSiftResult
    image: np.ndarray


@dataclass
class FormTemplates:
    templates: List[Template]


@dataclass
class Models:
    model_letters: Any
    model_numbers: Any
    letter_mapper: Dict
    number_mapper: Dict


@dataclass
class ProcessingConfig:
    models: Models
    templates: List[Template]
    form_structure: FormStructure


VALIDATION_EXCEL_NAME = "validation_excel.xlsx"
RESULT_EXCEL_NAME = "result.xlsx"


@dataclass
class PathsForProcessingConfig:
    template_path: str
    form_structure_path: str
    folder_with_documents_path: str
    final_excel_path: str = RESULT_EXCEL_NAME
    validation_excel_path: str = VALIDATION_EXCEL_NAME
    root: str = "."
