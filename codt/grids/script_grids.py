import argparse
import configparser

from alive_progress import alive_bar
from PIL import Image
import numpy as np

from drawing import draw_transp_line, opacity
from grids import make_grid, shake_that
from noise import get_noise
from utils import get_tuple_from_config


DEFAULT_CONFIG = 'default_grid_config.ini'


def get_linear(vmin, vmax, iterations, i):
    return vmin + i / (iterations * (vmax - vmin))


def compute(nodes, edges, noise_num, dev, primary_color):
    noise = get_noise(dev, (noise_num,) + nodes.shape)

    for i in range(iterations):
        nodes = shake_that(nodes, noise[i % noise_num], w=w, h=h)

        for n1, n2 in edges:
            shape = [tuple(nodes[n1]), tuple(nodes[n2])]
            draw_transp_line(img, shape, primary_color+opacity(get_linear(3, 10, iterations, i)), 3)
        yield


if __name__ == '__main__':

    # setup

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, default=None, dest='config')
    parser.add_argument('-f', '--file', type=str, default=None, dest='output_file')
    parser.add_argument('-s', '--show', action='store_true', dest='show',
                        help='Show histogram.')

    args = vars(parser.parse_args())
    config_file = args.get('config')
    show = args.get('show')

    config = configparser.ConfigParser()
    config.read(DEFAULT_CONFIG)
    if config_file:
        config.read(config_file)

    seed = config.getint('SETTINGS', 'np-seed')
    iterations = config.getint('SETTINGS', 'iterations')
    # filename = config.get('SETTINGS', 'filename')
    filename = '../../imgs/' + config.get('SETTINGS', 'filename')

    w = config.getint('SETTINGS', 'width')
    h = config.getint('SETTINGS', 'height')
    wn = config.getint('SETTINGS', 'node-columns-count')
    hn = config.getint('SETTINGS', 'node-rows-count')
    margin = config.getint('SETTINGS', 'margin')
    dev = config.getint('SETTINGS', 'dev')
    background_color = get_tuple_from_config(config, 'SETTINGS', 'background-color', int)
    primary_color = get_tuple_from_config(config, 'SETTINGS', 'primary-color', int)
    noise_num = config.getint('SETTINGS', 'noise-num')

    np.random.seed(seed)

    # run script

    nodes, edges = make_grid(w, h, wn=wn, hn=hn, m=margin)

    img = Image.new('RGBA', (w, h), background_color)

    with alive_bar(iterations) as bar:
        for i in compute(nodes, edges, noise_num, dev, primary_color):
            bar()

    img = img.convert("RGB")
    img.save(filename)
    if show:
        img.show()
