import copy
from dataclasses import dataclass
from typing import List

import cv2
import numpy as np

from fast_form.structure_parser.form_structure_dataclasses import FormPageData, FieldType, Orientation, Field


@dataclass
class PageStructureParser:
    """
    Gets imdata in cv2 image
    """
    page_structure: FormPageData

    def process_page(self, form_img) -> FormPageData:
        fields = []
        page_structure = copy.deepcopy(self.page_structure)

        for field in page_structure.fields:
            field_crops = self.process_field(field, form_img)
            fields.append(field_crops)

        page_structure.fields = fields
        return page_structure

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
