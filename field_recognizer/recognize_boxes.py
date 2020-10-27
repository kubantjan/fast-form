from typing import List

from pylab import *
from scipy.stats import norm

from field_recognizer.recognizing_dataclasses import RecognizingBoxResult, SingleChoiceStats, RecognizingResult
from structure_parser.form_structure_parser import FieldType, Field

logger = logging.getLogger(__name__)


def black_count(img: np.ndarray) -> int:
    return sum(sum(img == 0))


def recognize_single_choice_one_box(img: np.ndarray, single_choice_stats: SingleChoiceStats) -> RecognizingBoxResult:
    r = black_count(img)
    if r >= single_choice_stats.mu:
        is_full = True
        cdf = norm.cdf((r - single_choice_stats.mean_full) / single_choice_stats.var_full)

    else:
        is_full = False
        cdf = 1 - norm.cdf((r - single_choice_stats.mean_empty) / single_choice_stats.mean_empty)
    return RecognizingBoxResult(is_full, cdf, img)


def recognize_single_choice(imgs: List[np.ndarray], single_choice_stats: SingleChoiceStats) -> RecognizingResult:
    recognizing_box_results = [recognize_single_choice_one_box(img, single_choice_stats) for img in imgs]
    accuracies_of_selected_choices = [(i, box_result.accuracy) for i, box_result in enumerate(recognizing_box_results)
                                      if box_result.recognized]
    if len(accuracies_of_selected_choices) > 1:
        logger.warning("several possible selected choices boxes taking the blackest one")
        max_accuracy_tuple = max(accuracies_of_selected_choices, key=lambda x: x[1])
        selected = max_accuracy_tuple[0]
    elif len(accuracies_of_selected_choices) == 1:
        selected = accuracies_of_selected_choices[0][0]
    else:
        selected = -1
    return RecognizingResult(
        recognized=selected,
        recognizing_box_results=recognizing_box_results,
        accuracy=min(recognizing_box_results,
                     key=lambda recognizing_box_result: recognizing_box_result.accuracy).accuracy
    )


def calculate_box_stats(fields: List[Field]) -> SingleChoiceStats:
    boxes = [
        black_count(img) for field in fields for img in field.box_images if field.type == FieldType.SINGLE_CHOICE]
    mu = np.mean(boxes)
    empty = [box for box in boxes if box >= mu]
    full = [box for box in boxes if box <= mu]
    return SingleChoiceStats(mu, np.mean(empty), np.var(empty), np.mean(full), np.var(full))
