from os import path
import numpy as np
import cv2
HERE = path.abspath(path.dirname(__file__))

samples = np.loadtxt(path.join(HERE, 'data', 'train', 'generalsamples.data'), np.float32)
responses = np.loadtxt(path.join(HERE, 'data', 'train', 'generalresponses.data'), np.float32)
responses = responses.reshape((responses.size,1))

model = cv2.ml.KNearest_create()
model.train(samples,cv2.ml.ROW_SAMPLE, responses)
model.save(path.join(HERE, 'model', 'model.xml'))