import os
import tempfile
from typing import List, Tuple

import numpy as np
import openpyxl
import pandas as pd
from cv2 import cv2
from openpyxl import load_workbook

from structure_parser.form_structure_parser import FormData, FieldType


def output_data(form_datas: List[FormData]) -> Tuple[pd.DataFrame, List[np.ndarray]]:
    form_dict = dict()
    form_images = []
    question_number = 0
    for form_data in form_datas:
        for field in form_data.fields:
            field_dict = dict()
            if field.type == FieldType.BOXES:
                answer_index = int(np.argmax(np.array(field.recognized)))
                if field.answers:
                    answer = field.answers[answer_index]
                else:
                    answer = answer_index
            elif field.type == FieldType.LETTERS:
                answer = "".join(field.recognized)
            elif field.type == FieldType.NUMBERS:
                answer = "".join(field.recognized)
            else:
                raise AssertionError("Unexpected Field Type")

            field_dict['name'] = field.name
            field_dict['data'] = answer
            field_dict['acc'] = min(field.accuracy)
            form_images.append(field.img)
            form_dict[question_number] = field_dict
            question_number += 1

    df = pd.DataFrame.from_dict(form_dict, orient="index")
    return df, form_images


def save_data(df: pd.DataFrame, images: List[np.ndarray], document_path: str):
    with tempfile.TemporaryDirectory() as temp_image_folder:
        filename = f"{document_path.split('.')[0]}.xlsx"
        df.to_excel(filename)

        wb = load_workbook(filename=filename)
        ws = wb.worksheets[0]
        for i, img in zip(df.index, images):
            temp_image_path = os.path.join(temp_image_folder, f"{i}_img.png")
            height = 60
            ws.row_dimensions[i + 2].height = 50
            width = int(height / img.shape[0] * img.shape[1])
            dim = (width, height)
            resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


            cv2.imwrite(temp_image_path, resized)
            img = openpyxl.drawing.image.Image(temp_image_path)
            img.anchor = f'E{i + 2}'
            ws.add_image(img)
        wb.save(filename)
