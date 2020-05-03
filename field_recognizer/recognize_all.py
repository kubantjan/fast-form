from field_recognizer.recognize_letters import recognize_letters


def recognize_numbers(imgs):
    return [1] * len(imgs), [0.5] * len(imgs), imgs


def black_ratio(img):
    return sum(sum(img == 255))


def estimate_box(img, avg_ratio):
    r = black_ratio(img)
    return r <= avg_ratio, 0.9, img


def recognize_boxes(imgs, avg_ratio):
    return zip(*[estimate_box(img, avg_ratio) for img in imgs])


def calculate_black_ratio(fields):
    boxes = [black_ratio(img) for field in fields for img in field["box_data"] if field["type"] == "boxes"]
    return sum(boxes) / len(boxes)


def recognize(form_data: dict):
    avg_box_black_ratio = calculate_black_ratio(form_data["fields"])
    fields = []
    for field in form_data["fields"]:
        if field["type"] == "letters":
            recognized, accuracy, img_transf = recognize_letters(field["box_data"])
        elif field["type"] == "numbers":
            recognized, accuracy, img_transf = recognize_numbers(field["box_data"])
        elif field["type"] == "boxes":
            recognized, accuracy, img_transf = recognize_boxes(field["box_data"], avg_box_black_ratio)
        else:
            raise ValueError(f"Unknown field type {field['type']}")
        field["recognized"] = recognized
        field["accuracy"] = accuracy
        field["box_data_transf"] = img_transf
        fields.append(field)
    form_data["fields"] = fields
    return form_data
