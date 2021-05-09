# from simpleocr.files import open_image
# from simpleocr.grounding import UserGrounder
# from simpleocr.segmentation import ContourSegmenter
# import cv2

# image = cv2.imread(r'D:\Development\PyCharm\simple-ocr-opencv\simpleocr\data\1.png')
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# threshold = 160 # to be determined
# _, img_binarized = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
# cv2.imshow('f', img_binarized)
# key = cv2.waitKey(0)

##########################
import sys

import numpy as np
import cv2

im = cv2.imread(r'D:\Development\PyCharm\simple-ocr-opencv\simpleocr\data\train.png')
# im = cv2.imread(r'D:\Development\PyCharm\simple-ocr-opencv\data\pitrain.png')
im3 = im.copy()

gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(3,3),0)
# thresh = cv2.adaptiveThreshold(blur,255,1,1,11,2)
# thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,3,2)
threshold = 100
_, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)

# cv2.imshow('f', blur)
# cv2.imshow('f', thresh)
# key = cv2.waitKey(0)

#################      Now finding Contours         ###################

contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

samples =  np.empty((0,100))
responses = []
# keys = [i for i in range(48,58)]

for cnt in contours:
    if cv2.contourArea(cnt)>0: # and cv2.contourArea(cnt)<7:
        [x,y,w,h] = cv2.boundingRect(cnt)

        if  (h>14 and h<18 and w<14) or (h>0 and h<5 and w<5):
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
            roi = thresh[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(10,10))
            cv2.imshow('norm',im)
            key = cv2.waitKey(0)

            if key == 27:  # (escape to quit)
                sys.exit()
            # elif key in keys:
            else:
                responses.append(key)
                sample = roismall.reshape((1,100))
                samples = np.append(samples,sample,0)
        elif  h>0 and h<5 and w<5 and 1==5:
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),2)
            roi = thresh[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(10,10))
            cv2.imshow('norm',im)
            key = cv2.waitKey(0)

            if key == 27:  # (escape to quit)
                sys.exit()
            # elif key in keys:
            else:
                # print('key=',key)
                responses.append(key)
                sample = roismall.reshape((1,100))
                samples = np.append(samples,sample,0)

responses = np.array(responses,np.float32)
responses = responses.reshape((responses.size,1))
print ("training complete")

np.savetxt('generalsamples.data',samples)
np.savetxt('generalresponses.data',responses)