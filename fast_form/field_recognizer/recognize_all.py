from fast_form.config.configuration_dataclasses import Models
from fast_form.field_recognizer.recognize_boxes import calculate_box_stats, recognize_single_choice
from fast_form.field_recognizer.recognize_letters import recognize_chars
from fast_form.structure_parser.form_structure_dataclasses import FormPageData, FieldType


def recognize(form_data: FormPageData, models: Models) -> FormPageData:
    box_stats = calculate_box_stats(form_data.fields)
    fields = []
    for field in form_data.fields:
        if field.type == FieldType.LETTERS:
            field.recognizing_results = recognize_chars(field.box_images, models.model_letters,
                                                        models.letter_mapper)
        elif field.type == FieldType.NUMBERS:
            field.recognizing_results = recognize_chars(field.box_images, models.model_numbers,
                                                        models.number_mapper)
        elif field.type == FieldType.SINGLE_CHOICE:
            field.recognizing_results = recognize_single_choice(field.box_images, box_stats)
        else:
            raise ValueError(f"Unknown field type {field.type}")
        fields.append(field)
    form_data.fields = fields
    return form_data
