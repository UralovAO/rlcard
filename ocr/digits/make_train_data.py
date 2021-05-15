import sys
from os import path
import numpy as np
import cv2
HERE = path.abspath(path.dirname(__file__))

def preproccess_image(im):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (1, 1), 0)
    # blur = gray
    threshold = 130
    _, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
    return thresh

if __name__ == "__main__":

    im = cv2.imread(path.join(HERE, 'data', 'train', 'train.png'))
    # im3 = im.copy()

    preproccessed_image = preproccess_image(im)
    contours,hierarchy = cv2.findContours(preproccessed_image,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    samples =  np.empty((0,100))
    responses = []

    for cnt in contours:
        [x,y,w,h] = cv2.boundingRect(cnt)

        if  (h>14 and h<18 and w<14) or (h>1 and h<4 and w<4):
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
            roi = preproccessed_image[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(10,10))
            cv2.imshow('norm',im)
            key = cv2.waitKey(0)

            if key == 27:  # (escape to quit)
                sys.exit()
            else:
                responses.append(key)
                sample = roismall.reshape((1,100))
                samples = np.append(samples,sample,0)

    responses = np.array(responses,np.float32)
    responses = responses.reshape((responses.size,1))
    print ("Making training data is complete")

    np.savetxt(path.join(HERE, 'data', 'train', 'generalsamples.data'),samples)
    np.savetxt(path.join(HERE, 'data', 'train', 'generalresponses.data'),responses)