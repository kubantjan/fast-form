from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict

import numpy as np

from fast_form.field_recognizer.recognizing_dataclasses import RecognizingResult


@dataclass
class Point:
    x: int
    y: int


class Orientation(str, Enum):
    HORIZONTAL = 'HORIZONTAL'
    VERTICAL = 'VERTICAL'


class FieldType(str, Enum):
    LETTERS = 'LETTERS'
    NUMBERS = 'NUMBERS'
    SINGLE_CHOICE = 'SINGLE_CHOICE'


@dataclass
class Field:
    orientation: Orientation
    space_between_boxes: int
    number_of_boxes: int
    name: str
    type: FieldType
    top_left: Point
    bottom_right: Point
    img: Optional[np.ndarray] = None
    recognizing_results: Optional[RecognizingResult] = None
    box_images: Optional[List[np.ndarray]] = None


@dataclass
class FormPageData:
    fields: List[Field]


@dataclass
class FormStructure:
    form_page_data: Dict[str, FormPageData]
    page_count: int
