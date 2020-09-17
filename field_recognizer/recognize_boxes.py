from pylab import *
from scipy.stats import norm

from structure_parser.form_structure_parser import FieldType


def black_count(img):
    return sum(sum(img == 0))


def recognize_box(img, box_stats):
    r = black_count(img)
    mu, mu1, sigma1, mu2, sigma2 = box_stats
    if r >= mu:
        is_full = True
        cdf = norm.cdf((r - mu2) / sigma2)

    else:
        is_full = False
        cdf = 1 - norm.cdf((r - mu1) / sigma1)
    return is_full, cdf, img


def recognize_boxes(imgs, box_stats):
    return zip(*[recognize_box(img, box_stats) for img in imgs])


def calculate_box_stats(fields):
    boxes = [black_count(img) for field in fields for img in field.box_data if field.type == FieldType.BOXES]
    mu = np.mean(boxes)
    empty = [box for box in boxes if box >= mu]
    full = [box for box in boxes if box <= mu]
    return mu, np.mean(empty), np.var(empty), np.mean(full), np.var(full)
