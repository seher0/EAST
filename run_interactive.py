
import readline, argparse
import numpy as np
from PIL import Image

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')

from run_demo_server import get_predictor, save_result, config


def eval_image (predictor, img):
    '''
    image: numpy array (W, H, C)

    preproc image
    build model
    eval model
    postprocess image

    '''
    #img = np.transpose(img, (1, 0, 2)) #detects boxes but flipped outputs
    assert len(img.shape) == 3
    print (img.shape)

    rst = predictor(img)
    save_result(img, rst)


def eval_image_file (predictor, fname):
    im = Image.open(fname)
    eval_image(predictor, np.array(im))

def parse_args ():
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint_path', default='./east_icdar2015_resnet_v1_50_rbox/')
    parser.add_argument('--output', default='../output/')

    args = parser.parse_args()
    return args

def interactive_loop (args):
    config.SAVE_DIR = args.output
    predictor = get_predictor(args.checkpoint_path)
    while True:
        line = input('Enter Image path ("q" to quit): ')
        if line == 'q':
            break
        print ('File: "%s"' % line)
        eval_image_file(predictor, line.strip())


if __name__ == '__main__':
    args = parse_args() 
    interactive_loop (args)
