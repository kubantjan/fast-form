import cv2
import numpy as np


class FormStructureParser:
    """
    Gets imdata in cv2 image
    """

    def __init__(self, config):
        self.FormStructure = config

    def process_form(self, form_img):
        fields = []

        for field in self.FormStructure["fields"]:
            field_crops = self.process_field(field, form_img)
            fields.append(field_crops)

        form_data = self.FormStructure.copy()
        form_data["fields"] = fields
        return form_data

    def process_field(self, field_def, form):

        x1 = field_def["topLeft"]["x"]
        x2 = field_def["bottomRight"]["x"]
        y1 = field_def["topLeft"]["y"]
        y2 = field_def["bottomRight"]["y"]

        field_def["img"] = form[y1:y2, x1:x2]
        if field_def["orientation"] == "vertical":
            box_data = self.process_vertical_boxes(field_def)
        else:
            box_data = self.process_horizontal_boxes(field_def)

        field_def["box_data"] = box_data
        return field_def

    def process_horizontal_boxes(self, field_def):
        box_data = []
        field_img = field_def["img"]
        x1 = field_def["topLeft"]["x"]
        x2 = field_def["bottomRight"]["x"]
        space = field_def["spaceBetweenBoxes"]
        int_split = np.linspace(0, x2 - x1 + space, field_def["numberOfBoxes"] + 1)

        for xx1, xx2 in zip(int_split[:-1], int_split[1:]):
            box_img = field_img[:, int(xx1): int(xx2 - space / 2)]
            trimmed_box = self.trim_whitespace(box_img)
            box_data.append(trimmed_box)

        return box_data

    def process_vertical_boxes(self, field_def):
        box_data = []
        field_img = field_def["img"]
        y1 = field_def["topLeft"]["y"]
        y2 = field_def["bottomRight"]["y"]
        space = field_def["spaceBetweenBoxes"]
        int_split = np.linspace(0, y2 - y1 + space, field_def["numberOfBoxes"] + 1)
        for yy1, yy2 in zip(int_split[:-1], int_split[1:]):
            box_img = field_img[int(yy1 - space / 2): int(yy2 - space / 2), :]

            trimmed_box = self.trim_whitespace(box_img)
            box_data.append(trimmed_box)

        return box_data

    def trim_whitespace(self, img):

        gray = 255 * (img < 128).astype(np.uint8)
        coords = cv2.findNonZero(gray)  # Find all non-zero points (text)

        x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box
        rect = img[y:y + h, x:x + w]  # Crop the image
        return rect
