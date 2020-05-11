from field_recognizer.recognize_boxes import calculate_black_ratio, recognize_boxes
from field_recognizer.recognize_letters import recognize_chars


def recognize(form_data: dict, model_letters, model_numbers, letter_mapper, number_mapper):
    box_stats = calculate_black_ratio(form_data["fields"])
    print(box_stats)
    fields = []
    for field in form_data["fields"]:
        if field["type"] == "letters":
            recognized, accuracy, img_transf = recognize_chars(field["box_data"], model_letters, letter_mapper)
        elif field["type"] == "numbers":
            recognized, accuracy, img_transf = recognize_chars(field["box_data"], model_numbers, number_mapper)
        elif field["type"] == "boxes":
            recognized, accuracy, img_transf = recognize_boxes(field["box_data"], box_stats)
        else:
            raise ValueError(f"Unknown field type {field['type']}")
        field["recognized"] = recognized
        field["accuracy"] = accuracy
        field["box_data_transf"] = img_transf
        fields.append(field)
    form_data["fields"] = fields
    return form_data
