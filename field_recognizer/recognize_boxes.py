from pylab import *
from scipy.stats import norm


def black_ratio(img):
    return sum(sum(img == 255))


def estimate_box(img, box_stats):
    r = black_ratio(img)
    mu, mu1, sigma1, mu2, sigma2 = box_stats
    if r >= mu:
        is_full = False
        print(r)
        print(mu1)
        if r > mu1:
            cdf = 1
        else:
            cdf = 2 * norm.cdf((r - mu1) / sigma1)

    else:
        is_full = True
        if r < mu2:
            cdf = 1
        else:
            cdf = 2 * (1 - norm.cdf((r - mu2) / sigma2))
    return is_full, cdf, img


def recognize_boxes(imgs, box_stats):
    return zip(*[estimate_box(img, box_stats) for img in imgs])


def calculate_black_ratio(fields):
    boxes = [black_ratio(img) for field in fields for img in field["box_data"] if field["type"] == "boxes"]
    mu = np.mean(boxes)
    empty = [box for box in boxes if box >= mu]
    full = [box for box in boxes if box <= mu]
    print(boxes)
    return mu, np.mean(empty), np.var(empty), np.mean(full), np.var(full)
