import cv2

from fast_form.field_recognizer.recognizing_dataclasses import RecognizingBoxResult, RecognizingResult
from fast_form.field_recognizer.resizing_for_recognizers import resize

EMNIST_SIZE = 28
LETTER_BORDER = 2
COLOR_RANGE = 255
NUMBER_OF_PIXELS_FOR_SPACE = 20


def is_not_space(img):
    if len(img) == 0:
        return False
    return sum(sum(img == 0)) > NUMBER_OF_PIXELS_FOR_SPACE


# not used anymore as it did not help performance
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
        img,
        EMNIST_SIZE,
        LETTER_BORDER
    )


def recognize_chars(imgs, model, result_mapper) -> RecognizingResult:
    recognizing_box_results = [recognize_char(preprocess_img(img), model, result_mapper) for img in imgs]
    return RecognizingResult(
        accuracy=min(recognizing_box_results,
                     key=lambda recognizing_box_result: recognizing_box_result.accuracy).accuracy,
        recognizing_box_results=recognizing_box_results,
        recognized="".join([res.recognized for res in recognizing_box_results])
    )


def recognize_char(img, model, result_mapper) -> RecognizingBoxResult:
    if is_not_space(img):
        img_p = img.copy()
        img_p = prepare_for_model_format(img_p)
        prediction, accuracy = predict(img_p, model, result_mapper)
        return RecognizingBoxResult(prediction, accuracy, img)
    else:
        return RecognizingBoxResult(" ", 1.0, img)


def predict(img, model, result_mapper):
    pred = model.predict(img)
    pred_val = result_mapper.get(pred[0].argmax())
    accuracy = pred[0].max()
    return pred_val, accuracy


def prepare_for_model_format(img):
    img = 1 - (img.reshape(1, EMNIST_SIZE, EMNIST_SIZE, 1).transpose() / COLOR_RANGE)
    return img
