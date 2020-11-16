from typing import List

from fast_form.structure_parser.form_structure_dataclasses import Field, Orientation, FieldType, Point


def get_fields_for_page(
        questions_per_page: int,
        y_start: int,
        x_start: int,
        width: int,
        line_step: int,
        line_height: int,
        first_question_number: int) -> List[Field]:
    fields = []
    question_number = first_question_number
    for i in range(questions_per_page):
        fields.append(
            Field(
                orientation=Orientation.HORIZONTAL,
                space_between_boxes=80,
                name=f"{question_number}",
                type=FieldType.SINGLE_CHOICE,
                top_left=Point(x_start, y_start + i * line_step),
                bottom_right=Point(x_start + width, y_start + line_height + i * line_step),
                number_of_boxes=4
            )
        )
        question_number += 1
    return fields
