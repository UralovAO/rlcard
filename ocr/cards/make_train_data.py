import sys
from os import path
import numpy as np
import cv2
from glob import glob
HERE = path.abspath(path.dirname(__file__))

pictures_path = sorted(glob(path.join(HERE, 'data', 'pictures', '*.png')))
for picture_path in pictures_path:
    rank_value = picture_path.replace('.png', '')[-2:]
    # get digit representation of rank and value of card
    digit_rank_value = str(ord(card_value[0]))+str(ord(card_value[1]))
    # rank = [115, 104, 100, 99]

    # print(card_value)
    print(ord(card_value[0]))
    # print(ord(card_value[1]))
    print(str(ord(card_value[0]))+str(ord(card_value[1])))
    print(' ')

