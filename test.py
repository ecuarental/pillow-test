"""
Testing PILLOW
"""

import logging
from glob import glob
from os import path

from PIL import Image

logging.basicConfig(level=logging.INFO)

RESOURCES_FOLDER = 'resources/'
INPUT_FOLDER = path.join(RESOURCES_FOLDER, 'input/')
OUTPUT_FOLDER = path.join(RESOURCES_FOLDER, 'output/')
OUTPUT_EXTENSION = '.jpeg'
DESIRED_SIZE = (1920, 1080)
WIDTH, HEIGHT = DESIRED_SIZE
DESIRED_RATIO = WIDTH / HEIGHT

for filename in glob(INPUT_FOLDER + '*.jpeg'):

    logging.info('Opening the file %s', filename)
    im = Image.open(filename)

    filename_base = path.basename(filename).split('.')[0]
    logging.info('The base filename is %s', filename_base)

    x, y = im.size
    logging.info('The image size has %d width %d height', x, y)
    aspect_ratio = x/y
    logging.info('The aspect ratio is %2f', aspect_ratio)
    logging.info('The desired aspect ratio is %2f', DESIRED_RATIO)

    if aspect_ratio > DESIRED_RATIO:
        logging.info('It is a wider image')
        width = round(HEIGHT * aspect_ratio)
        logging.info('The transformed image size is %d x %d', width, HEIGHT)
        im = im.resize((width, HEIGHT), resample=Image.NEAREST)

        width_dif = width - WIDTH
        logging.info('The width difference is %d', width_dif)

        box = (
            round(width_dif / 2),
            0,
            WIDTH,
            HEIGHT
        )

        im = im.crop(box)

    else:
        logging.info('It is a taller image')
        height = round(WIDTH / aspect_ratio)
        logging.info('The transformed image size is %d x %d', WIDTH, height)
        im = im.resize((WIDTH, height), resample=Image.NEAREST)

        height_dif = height - HEIGHT
        logging.info('The height difference is %d', height_dif)

        box = (
            0,
            round(height_dif / 2),
            WIDTH,
            HEIGHT
        )

        im = im.crop(box)

    im_w, im_y = im.size
    logging.info('The cropped image is %d x %d', im_w, im_y)

    filename_output = path.join(
        OUTPUT_FOLDER, filename_base + OUTPUT_EXTENSION)
    logging.info('The output filename is %s', filename_output)

    im.save(filename_output)
    logging.info('The output filename was saved successfully')
