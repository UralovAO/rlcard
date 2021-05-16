import sys
from os import path
import numpy as np
import cv2
from glob import glob
HERE = path.abspath(path.dirname(__file__))

pictures_path = sorted(glob(path.join(HERE, 'data', 'pictures', '*.png')))

responses = []
samples = np.empty((0,300))

for picture_path in pictures_path:
    print('picture_path = ', picture_path)
    rank_value = picture_path.replace('.png', '')[-2:]
    # get digit representation of rank and value of card
    digit_rank_value = str(ord(rank_value[0]))+str(ord(rank_value[1]))
    # ranks = [115, 104, 100, 99]
    responses.append(digit_rank_value)


    sample = cv2.imread(picture_path)
    sample = cv2.resize(sample, (10, 10))
    # print('sample.shape = ', sample.shape)
    # assert 11==2
    sample = sample.reshape((1,300))
    samples = np.append(samples, sample, 0)

responses = np.array(responses, np.float32)
responses = responses.reshape((responses.size, 1))
print("Making training data is complete")

np.savetxt(path.join(HERE, 'data', 'train', 'generalsamples.data'), samples)
np.savetxt(path.join(HERE, 'data', 'train', 'generalresponses.data'), responses)
