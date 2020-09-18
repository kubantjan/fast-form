from dataclasses import dataclass
from typing import List, Any, Dict

import cv2
import numpy as np


@dataclass
class ImageSiftResult:
    key_points: List[cv2.KeyPoint]
    descriptions: np.ndarray


@dataclass
class Template:
    sift_result: ImageSiftResult
    image: np.ndarray


@dataclass
class Configuration:
    template: Template


@dataclass
class PathConfig:
    template_image_path: str
    form_structure_config_path: str
    model_data_location: str = "./model_data"


@dataclass
class Models:
    model_letters: Any
    model_numbers: Any
    letter_mapper: Dict
    number_mapper: Dict
