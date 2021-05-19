import cv2
import numpy as np
from os import path

HERE = path.abspath(path.dirname(__file__))

# def get_number(image_path = 'data/2.png'):
def get_card(im):
    model = cv2.ml.KNearest_load(path.join(HERE, 'model', 'model.xml'))

    # im = cv2.imread(image_path)
    # cv2.imshow('out',im)
    # cv2.waitKey(0)

    sample = cv2.resize(im, (10, 10))
    sample = sample.reshape((1, 300))
    sample = np.float32(sample)

    retval, results, neigh_resp, dists = model.findNearest(sample, k = 1)
    digit_rank_value = str(int(results[0][0]))
    if digit_rank_value[:2] == '99':
        rank = 'c'
        value = chr(int(digit_rank_value[2:]))
        rank_value = rank + value
    elif digit_rank_value[:3] == '104':
        rank = 'h'
        value = chr(int(digit_rank_value[3:]))
        rank_value = rank + value
    elif digit_rank_value[:3] == '115':
        rank = 's'
        value = chr(int(digit_rank_value[3:]))
        rank_value = rank + value
    elif digit_rank_value[:3] == '100':
        rank = 'd'
        value = chr(int(digit_rank_value[3:]))
        rank_value = rank + value
    elif digit_rank_value[:3] == '103':
        rank_value = None
    else:
        sys.exit('Application: rank is incorrect')

    # print('rank_value = ', rank_value)

    return rank_value

# get_number()