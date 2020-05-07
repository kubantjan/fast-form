import cv2
import numpy as np

from field_recognizer.resizing_for_recognizers import resize

EMNIST_SIZE = 28
LETTER_BORDER = 2


def is_not_space(img):
    if len(img) == 0:
        return False
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
        EMNIST_SIZE,
        LETTER_BORDER
    )


def recognize_chars(imgs, model, result_mapper):
    res = [recognize_char(preprocess_img(img), model, result_mapper) if is_not_space(img) else (" ", 1.0, img) for img
           in imgs]

    return zip(*res)


def recognize_char(img, model, result_mapper):
    img_p = img.copy()
    img_p = prepare_for_model_format(img_p)
    prediction = predict(img_p, model, result_mapper)
    return prediction, 0.5, img


def predict(img, model, result_mapper):
    pred = model.predict(np.array([img]))
    pred_val = result_mapper.get(pred[0].argmax())
    return pred_val


def prepare_for_model_format(img):
    img = cv2.bitwise_not(img)
    img = img.transpose()
    img = img.ravel()
    img = img.astype('int64')
    return img
