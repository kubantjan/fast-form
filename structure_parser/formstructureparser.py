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
        boxCount = field_def["numberOfBoxes"]
        if field_def["orientation"] == "horizontal":
            x = field_def["topLeft"]["x"]
            width = field_def["boxWidth"] * boxCount + field_def['spaceBetweenBoxes'] * (boxCount - 1)
            y = field_def["topLeft"]["y"]
            height = field_def["boxHeight"]
            field_def["img"] = form[y:y + height, x:x + width]

            box_data = self.processHorizontalBoxes(field_def)

        elif field_def["orientation"] == "vertical":
            x = field_def["topLeft"]["x"]
            width = field_def["boxWidth"]
            y = field_def["topLeft"]["y"]
            height = field_def["boxHeight"] * boxCount + field_def['spaceBetweenBoxes'] * (boxCount - 1)
            field_def["img"] = form[y:y + height, x:x + width]
            box_data = self.processVerticalBoxes(field_def)
        else:
            m = "Attribute 'orientation' in form structure format have to be 'vertical' or 'horizontal'"
            raise ValueError(m)

        field_def["box_data"] = box_data
        return field_def

    def processHorizontalBoxes(self, field_def):
        x = 0
        box_data = []
        field_img = field_def["img"]

        for i in range(field_def["numberOfBoxes"]):
            w = field_def["boxWidth"]
            step = w + field_def["spaceBetweenBoxes"]
            box_img = field_img[:, x:x + w]
            trimmed_box = self.trim_whitespace(box_img)
            box_data.append(trimmed_box)
            x = x + step

        return box_data

    def processVerticalBoxes(self, field_def):
        y = 0
        box_data = []
        field_img = field_def["img"]

        for i in range(field_def["numberOfBoxes"]):
            h = field_def["boxHeight"]
            step = h + field_def["spaceBetweenBoxes"]
            box_img = field_img[y:y + h, :]
            trimmed_box = self.trim_whitespace(box_img)
            box_data.append(trimmed_box)
            y = y + step

        return box_data

    def trim_whitespace(self, img):

        gray = 255 * (img < 128).astype(np.uint8)
        coords = cv2.findNonZero(gray)  # Find all non-zero points (text)

        x, y, w, h = cv2.boundingRect(coords)  # Find minimum spanning bounding box
        rect = img[y:y + h, x:x + w]  # Crop the image - note we do this on the original image
        return rect
