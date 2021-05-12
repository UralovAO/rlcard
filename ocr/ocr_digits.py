import cv2
import numpy as np
from os import path
from .make_train_data import preproccess_image

HERE = path.abspath(path.dirname(__file__))

# def get_number(image_path = 'data/2.png'):
def get_number(im, player_id=0):
    # print('player_id=',player_id)
    model = cv2.ml.KNearest_load(path.join(HERE, 'model','model.xml'))

    # im = cv2.imread(image_path)
    preproccessed_image = preproccess_image(im)
    # cv2.imwrite(f'preproccessed_image{player_id}.png', preproccessed_image)
    # cv2.imshow('out',preproccessed_image)
    # cv2.waitKey(0)
    # gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    # blur = cv2.GaussianBlur(gray,(3,3),0)
    # threshold = 100
    # _, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
    contours,hierarchy = cv2.findContours(preproccessed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    out = np.zeros(im.shape, np.uint8)
    digits = []

    for cnt in contours:
        if cv2.contourArea(cnt)>0:
            [x,y,w,h] = cv2.boundingRect(cnt)
            if  (h>14 and h<18 and w<14) or (h>1 and h<4 and w<4):
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                roi = preproccessed_image[y:y+h,x:x+w]
                roismall = cv2.resize(roi,(10,10))
                roismall = roismall.reshape((1,100))
                roismall = np.float32(roismall)
                retval, results, neigh_resp, dists = model.findNearest(roismall, k = 1)
                string = str(chr(results[0][0]))
                digits.append((x, string))
                # print('string = ', string)
                cv2.putText(out,string,(x,y+h),0,1,(0,255,0))
    digits = sorted(digits)
    # print('digits = ', digits)
    result_number = [x[1] for x in digits]
    result_number = "".join(result_number)
    # print('result_number = ', result_number)
    if result_number != '':
        result_number = float(result_number)
    else:
        result_number = None

    # cv2.imwrite(f'im{player_id}.png', im)

    # cv2.imshow('im',im)
    # cv2.waitKey(0)

    return result_number


    # cv2.imshow('im',im)
    # cv2.imshow('out',out)
    # cv2.waitKey(0)

# get_number()