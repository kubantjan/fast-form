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
    recognized: Union[str, bool]
    recognizing_box_results: List[RecognizingBoxResult]
    accuracy: float


@dataclass
class SingleChoiceStats:
    mu: float
    mean_empty: float
    var_empty: float
    mean_full: float
    var_full: float
