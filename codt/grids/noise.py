import numpy as np


def get_noise(dev, shape, batch=1):
    return np.random.randint(-dev, dev, shape)
