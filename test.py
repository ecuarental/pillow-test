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
OUTPUT_EXTENSION = '.jpg'
INPUT_EXTENSION = '.jpg'
DESIRED_SIZE = (1280, 720)
'''
1920 x 1080
1280 x 720
'''
WIDTH, HEIGHT = DESIRED_SIZE
DESIRED_RATIO = WIDTH / HEIGHT
KEEP_NAME = True
BASENAME = 'marketing'
COUNTER_START = 1


def resize_img(img_file, output_size):
    """Resize image"""
    out_width, out_height = output_size
    out_ratio = out_width / out_height

    logging.info('Opening the file %s', img_file)
    image = Image.open(img_file)
    w, h = image.size
    logging.info('The image size has %d width %d height', w, h)
    ratio = w/h
    logging.info('The aspect ratio is %2f', ratio)
    logging.info('The desired aspect ratio is %2f', out_ratio)

    if ratio > out_ratio:
        logging.info('It is a wider image')
        width = round(out_height * ratio)
        height = out_height
        logging.info('The transformed image size is %d x %d',
                     width, height)
        image = image.resize((width, height), resample=Image.NEAREST)

    else:
        logging.info('It is a taller image')
        height = round(out_width / ratio)
        width = out_width
        logging.info('The transformed image size is %d x %d',
                     width, height)
        image = image.resize((width, height), resample=Image.NEAREST)

    width_dif = width - out_width
    logging.info('The width difference is %d', width_dif)
    height_dif = height - out_height
    logging.info('The height difference is %d', height_dif)

    width_offset = round(width_dif / 2)
    height_offset = round(height_dif / 2)

    box = (
        width_offset,
        height_offset,
        out_width + width_offset,
        out_height + height_offset
    )

    logging.info('The box is %s', box)
    image = image.crop(box)

    im_w, im_y = image.size
    logging.info('The cropped image is %d x %d', im_w, im_y)

    return image


for count, filename in enumerate(glob(INPUT_FOLDER + '*' + INPUT_EXTENSION)):

    out_image = resize_img(filename, DESIRED_SIZE)

    if KEEP_NAME:
        filename_base = path.basename(filename).split('.')[0]
    else:
        count += COUNTER_START
        filename_base = f'{BASENAME}_{count:02d}'

    filename_output = path.join(
        OUTPUT_FOLDER, filename_base + OUTPUT_EXTENSION)
    logging.info('The output filename is %s', filename_output)

    out_image.save(filename_output)
    logging.info('The output filename was saved successfully')
