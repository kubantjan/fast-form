from field_recognizer.resizing_for_recognizers import resize_letter


def is_not_space(img):
    print(img.shape)

    return min(img.shape) > 2


def recognize_letters(imgs):
    res = [recognize_letter(resize_letter(img)) if is_not_space(img) else ("", 1.0) for img in imgs]

    return zip(*res)


def recognize_letter(resized_img):
    # TODO ADAM
    return "c", 0.5
