
import argparse, os
import numpy as np
from pathlib import Path
from PIL import Image

import logging 
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)

import readline
readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')

from run_demo_server import get_predictor, save_result, config
from gsi.process_pdf import pdf2png


def eval_image (predictor, img):
    '''
    image: numpy array (H, W, C)

    preproc image
    build model
    eval model
    postprocess image

    '''
    #img = np.transpose(img, (1, 0, 2)) #detects boxes but flipped outputs
    assert len(img.shape) == 3
    logger.warn ('shape = ' + str(img.shape) )

    shape = img.shape
    if shape[0] < shape[1]: 
        logger.info ('Expecting HWC format, with H > W')
        return

    rst = predictor(img)
    save_result(img, rst)

    dirpath = os.path.join(config.SAVE_DIR, rst['session_id'])
    logger.warn ('Saving result to path : ' + dirpath)


def eval_image_file (predictor, fname):
    im = Image.open(fname)
    eval_image(predictor, np.array(im))

def eval_pdf_file (predictor, fname):
    logger.warn ('\n** Evaluating pdf file : ' + fname)
    img_np_arrs = pdf2png (fname)

    for im in img_np_arrs:
        eval_image (predictor, im)

def parse_args ():
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint_path', default='./east_icdar2015_resnet_v1_50_rbox/')
    parser.add_argument('--output', default='../output/')

    args = parser.parse_args()
    return args

def interactive_loop (predictor):
    while True:
        line = input('Enter Image path ("q" to quit): ')
        line = line.strip()
        if line == 'q':
            break
        logger.info ('File: "%s"' % line)

        path = Path(line)
        if path.suffix == '.png':
            eval_image_file(predictor, str(path))
        elif path.suffix == '.pdf':
            eval_pdf_file (predictor, str(path))

def try_all_user_pdfs (predictor):
    base = Path('/WS/data/1 - user uploaded pdfs/')
    #print (base)
    for p in list(base.glob('*.pdf')):
        eval_pdf_file (predictor, str(p))


if __name__ == '__main__':
    args = parse_args() 
    config.SAVE_DIR = args.output
    predictor = get_predictor(args.checkpoint_path)

    #interactive_loop (args)
    try_all_user_pdfs (predictor)