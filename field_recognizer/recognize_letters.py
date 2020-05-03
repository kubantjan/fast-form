import cv2

from field_recognizer.resizing_for_recognizers import resize

EMNIST_SIZE = 28


def is_not_space(img):
    return sum(sum(img == 0)) > 30


def thicken(img):
    new_img = cv2.bitwise_not(
        cv2.dilate(
            cv2.bitwise_not(img),
            cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)),
            iterations=1
        )
    )
    return new_img


def preprocess_img(img):
    return resize(
        thicken(img),
        EMNIST_SIZE
    )


def recognize_letters(imgs):
    res = [recognize_letter(preprocess_img(img)) if is_not_space(img) else (" ", 1.0, img) for img in imgs]

    return zip(*res)


def recognize_letter(resized_img):
    # TODO ADAM
    return "c", 0.5, resized_img
