def recognize_letters(imgs):
    return ["a"] * len(imgs), [0.5] * len(imgs)


def recognize_numbers(imgs):
    return [1] * len(imgs), [0.5] * len(imgs)


def recognize_boxes(imgs):
    return [True] * len(imgs), [0.5] * len(imgs)


def recognize(form_data: dict):
    fields = []
    for field in form_data["fields"]:
        if field["type"] == "letters":
            recognized, accuracy = recognize_letters(field["box_data"])
        elif field["type"] == "numbers":
            recognized, accuracy = recognize_numbers(field["box_data"])
        elif field["type"] == "boxes":
            recognized, accuracy = recognize_boxes(field["box_data"])
        else:
            raise ValueError(f"Unknown field type {field['type']}")
        field["recognized"] = recognized
        field["accuracy"] = accuracy
        fields.append(field)
    form_data["fields"] = fields
    return form_data
