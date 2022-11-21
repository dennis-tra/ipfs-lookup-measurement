# import scipy.constants as sc
import numpy as np

linewidth_pt = 241.14749


def figsize(scale, heightRatio=1/1.5):
    inches_per_pt = 1 / 72.27
    textwidthInInch = inches_per_pt * linewidth_pt
    figWidthInInch = textwidthInInch * scale
    figHeightInInch = figWidthInInch * heightRatio
    return [figWidthInInch, figHeightInInch]


def calc_cdf_x(values):
    return np.append(np.sort(values), max(values))


def calc_cdf_y(values):
    return np.linspace(0, 1, len(values) + 1)
