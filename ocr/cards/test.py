import cv2
from os import path
import numpy as np
# from make_train_data import preproccess_image

# def get_number(image_path = 'data/2.png'):

HERE = path.abspath(path.dirname(__file__))

def get_number(image_path):

    model = cv2.ml.KNearest_load(path.join(HERE, 'model', 'model.xml'))

    im = cv2.imread(image_path)
    # preproccessed_image = preproccess_image(im)
    #
    cv2.imshow('out',im)
    cv2.waitKey(0)

    sample = cv2.resize(im, (10, 10))
    cv2.imshow('sample',sample)
    cv2.waitKey(0)
    sample = sample.reshape((1, 300))
    sample = np.float32(sample)

    retval, results, neigh_resp, dists = model.findNearest(sample, k = 1)
    # string = str(chr(results[0][0]))
    digit_rank_value = str(int(results[0][0]))
    print('digit_rank_value = ', digit_rank_value)
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

    print('rank_value = ', rank_value)
    # ranks = {'s':115, 'h':104, 'd':100, 'c':99}

    # digits.append((x, string))
    #             print('string = ', string)
    # cv2.putText(out,string,(x,y+h),0,1,(0,255,0))
    # digits = sorted(digits)
    # print('digits = ', digits)
    # result_number = [x[1] for x in digits]
    # result_number = "".join(result_number)
    # print('result_number = ', result_number)
    # result_number = float(result_number)


    # cv2.imshow('im',im)
    # cv2.imwrite('data/im.png', im)
    # cv2.imshow('out',out)
    # cv2.waitKey(0)

    return rank_value

# get_number(r'D:\Development\PyCharm\rlcard\screenshots/screen_digits_3_PIL.png')
get_number(path.join(HERE, 'data', 'pictures', 'h4.png'))