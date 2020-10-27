import copy
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Dict

import cv2
import dacite
import numpy as np
from dacite import Config

from field_recognizer.recognizing_dataclasses import RecognizingResult


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
class FormData:
    fields: List[Field]


class FormStructureParser:
    """
    Gets imdata in cv2 image
    """

    def __init__(self, config: Dict):
        self.form_structure = dacite.from_dict(data_class=FormData, data=config,
                                               config=Config(cast=[FieldType, Orientation]))

    def process_form(self, form_img) -> FormData:
        fields = []
        form_structure = copy.deepcopy(self.form_structure)

        for field in form_structure.fields:
            field_crops = self.process_field(field, form_img)
            fields.append(field_crops)

        form_structure.fields = fields
        return form_structure

    def process_field(self, field_def: Field, form):

        x1 = field_def.top_left.x
        x2 = field_def.bottom_right.x
        y1 = field_def.top_left.y
        y2 = field_def.bottom_right.y

        field_def.img = form[y1:y2, x1:x2]
        if field_def.orientation == Orientation.VERTICAL:
            box_data = self.process_vertical_boxes(field_def)
        else:
            box_data = self.process_horizontal_boxes(field_def)

        field_def.box_images = box_data
        return field_def

    def process_horizontal_boxes(self, field_def: Field) -> List[np.ndarray]:
        box_data = []
        field_img = field_def.img
        x1 = field_def.top_left.x
        x2 = field_def.bottom_right.x
        space = field_def.space_between_boxes
        int_split = np.linspace(0, x2 - x1, field_def.number_of_boxes + 1)

        for xx1, xx2 in zip(int_split[:-1], int_split[1:]):
            box_img = field_img[:, int(xx1) + int(space / 2): int(xx2 - space / 2)]
            trimmed_box = self.trim_whitespace(box_img, field_def.type)
            box_data.append(trimmed_box)
        return box_data

    def process_vertical_boxes(self, field_def: Field) -> List[np.ndarray]:
        box_data = []
        field_img = field_def.img
        y1 = field_def.top_left.y
        y2 = field_def.bottom_right.y
        space = field_def.space_between_boxes
        int_split = np.linspace(0, y2 - y1 + space, field_def.number_of_boxes + 1)
        for yy1, yy2 in zip(int_split[:-1], int_split[1:]):
            box_img = field_img[int(yy1 - space / 2): int(yy2 - space / 2), :]

            trimmed_box = self.trim_whitespace(box_img, field_def.type)
            box_data.append(trimmed_box)

        return box_data

    @staticmethod
    def trim_whitespace(img: np.ndarray, field_type: FieldType) -> np.ndarray:
        if field_type is FieldType.SINGLE_CHOICE:
            return img

        gray = 255 * (img < 128).astype(np.uint8)
        coords = cv2.findNonZero(gray)  # Find all non-zero points (text)

        x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box
        trimmed_img = img[y:y + h, x:x + w]  # Crop the image
        return trimmed_img
