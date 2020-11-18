import logging
from typing import List

import numpy as np

from fast_form.field_recognizer.recognizing_dataclasses import RecognizingBoxResult, SingleChoiceStats, \
    RecognizingResult
from fast_form.structure_parser.form_structure_dataclasses import Field, FieldType

logger = logging.getLogger(__name__)

MULTIPLE_RESPONSES_FOUND = -1
NO_RESPONSE_FOUND = -2


def black_count_ratio(img: np.ndarray) -> int:
    ratio = sum(sum(img == 0)) / img.size
    assert 1 > ratio > 0
    return ratio


def recognize_single_choice_one_box(img: np.ndarray, single_choice_stats: SingleChoiceStats) -> RecognizingBoxResult:
    r = black_count_ratio(img)
    if r >= single_choice_stats.split_between:
        is_full = True
        dist = single_choice_stats.mean_full - single_choice_stats.split_between
        accuracy = np.clip(((r - single_choice_stats.split_between) - (single_choice_stats.mean_full - r)) / dist,
                           a_min=0,
                           a_max=1
                           )

    else:
        is_full = False
        dist = single_choice_stats.split_between - single_choice_stats.mean_empty
        accuracy = np.clip(((single_choice_stats.split_between - r) - (r - single_choice_stats.mean_empty)) / dist,
                           a_min=0,
                           a_max=1
                           )
    return RecognizingBoxResult(is_full, accuracy, img)


def recognize_single_choice(imgs: List[np.ndarray], single_choice_stats: SingleChoiceStats) -> RecognizingResult:
    recognizing_box_results = [recognize_single_choice_one_box(img, single_choice_stats) for img in imgs]
    accuracies_of_selected_choices = [(i, box_result.accuracy) for i, box_result in enumerate(recognizing_box_results)
                                      if box_result.recognized]
    if len(accuracies_of_selected_choices) > 1:
        logger.debug(
            f"Several possible selected choice boxes: {[i for i, _ in accuracies_of_selected_choices]},"
            f" returning {MULTIPLE_RESPONSES_FOUND}")
        selected = MULTIPLE_RESPONSES_FOUND
    elif len(accuracies_of_selected_choices) == 1:
        selected = accuracies_of_selected_choices[0][0]
    else:
        logger.debug(f"No possible selected choice boxes, returning {NO_RESPONSE_FOUND}")
        selected = NO_RESPONSE_FOUND
    return RecognizingResult(
        recognized=selected,
        recognizing_box_results=recognizing_box_results,
        accuracy=min(recognizing_box_results,
                     key=lambda recognizing_box_result: recognizing_box_result.accuracy).accuracy
    )


def calculate_box_stats(fields: List[Field]) -> SingleChoiceStats:
    black_ratios = [
        black_count_ratio(img) for field in fields for img in field.box_images if field.type == FieldType.SINGLE_CHOICE]

    average_blackness = np.mean(black_ratios)
    empty_mean_first_approximation = np.mean([box for box in black_ratios if box <= average_blackness])
    full_mean_first_approximation = np.mean([box for box in black_ratios if box >= average_blackness])
    split_between_first_approximation = (empty_mean_first_approximation + full_mean_first_approximation) / 2

    empty_mean = np.mean([box for box in black_ratios if box <= split_between_first_approximation])
    full_mean = np.mean([box for box in black_ratios if box >= split_between_first_approximation])
    split_between = (empty_mean + full_mean) / 2

    return SingleChoiceStats(mean_empty=empty_mean, mean_full=full_mean, split_between=split_between)
