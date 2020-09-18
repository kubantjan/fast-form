import os

import cv2
import numpy as np
import pandas as pd

from structure_parser.form_structure_parser import FormData, FieldType
from pathlib import Path


def output_data(form_data: FormData, document_path: str) -> str:
    d = dict()
    output_dir = os.path.join(os.path.dirname(document_path), "output")
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for field in form_data.fields:
        if field.type == FieldType.BOXES:
            data = field.answers[np.argmax(np.array(field.recognized))]
        elif field.type == FieldType.LETTERS:
            data = "".join(field.recognized)
        elif field.type == FieldType.NUMBERS:
            data = "".join(field.recognized)

        field_name = field.name
        d[f'{field_name}_data'] = data,
        d[f'{field_name}_acc'] = min(field.accuracy)
        d[f'{field_name}_img'] = f"{field_name}_img.png"
        cv2.imwrite(os.path.join(output_dir, f"{field_name}_img.png"), field.img)

    df = pd.DataFrame(d)
    filename = f"{document_path.split('.')[0]}.xlsx"
    df.to_excel(filename, index=False)
    return filename
