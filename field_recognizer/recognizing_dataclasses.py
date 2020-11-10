from dataclasses import dataclass
from typing import Union, List

import numpy as np


@dataclass
class RecognizingBoxResult:
    recognized: Union[str, bool, int]
    accuracy: float
    img_transf: np.ndarray


@dataclass
class RecognizingResult:
    recognized: Union[int, bool]
    recognizing_box_results: List[RecognizingBoxResult]
    accuracy: float


@dataclass
class SingleChoiceStats:
    split_between: float
    mean_empty: float
    mean_full: float
