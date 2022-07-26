import numpy as np


def make_grid(w, h, wn, hn, m=0):
    """
    m stands for margin
    """
    if 2 * m >= w or 2 * m >= h:
        raise Exception('too big margin.')

    w -= 2 * m
    h -= 2 * m

    nodes = np.array([
        [m + i * (w / (wn+1)), m + j * (h / (hn+1))] for i in range(1, wn+1) for j in range(1, hn+1)
    ])
    # edges = [(i+j*wn, i+1+j*hn) for i in range(0, wn-1) for j in range(0, wn)]
    # vertical edges
    vedges = [(j + i*hn, j+1 + i*hn) for j in range(hn-1) for i in range(wn)]
    # horizontal edges
    hedges = [(j+i*hn, j+(i+1) * hn) for j in range(hn) for i in range(wn-1)]
    return nodes, vedges + hedges


def shake_that(arr, noise=None, mode='n', w=None, h=None):
    """
    modes:
    n - normal
    b - bounce
    s - sticky
    """
    out = arr + noise
    if mode == 's':
        if not w and h:
            raise Exception('ey, w and h needed.')
        out[out < 0] = 100

    return out
