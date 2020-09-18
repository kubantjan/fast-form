from config.configuration import Models
from field_recognizer.recognize_boxes import calculate_box_stats, recognize_boxes
from field_recognizer.recognize_letters import recognize_chars
from structure_parser.form_structure_parser import FormData, FieldType


def recognize(form_data: FormData, models: Models) -> FormData:
    box_stats = calculate_box_stats(form_data.fields)
    fields = []
    for field in form_data.fields:
        if field.type == FieldType.LETTERS:
            recognized, accuracy, img_transf = recognize_chars(field.box_data, models.model_letters,
                                                               models.letter_mapper)
        elif field.type == FieldType.NUMBERS:
            recognized, accuracy, img_transf = recognize_chars(field.box_data, models.model_numbers,
                                                               models.number_mapper)
        elif field.type == FieldType.BOXES:
            recognized, accuracy, img_transf = recognize_boxes(field.box_data, box_stats)
        else:
            raise ValueError(f"Unknown field type {field.type}")
        field.recognized = recognized
        field.accuracy = accuracy
        field.box_data_transf = img_transf
        fields.append(field)
    form_data.fields = fields
    return form_data
