import cv2
import numpy as np
from make_train_data import preproccess_image

# def get_number(image_path = 'data/2.png'):
def get_number(image_path):

    model = cv2.ml.KNearest_load("model/model.xml")

    im = cv2.imread(image_path)
    # preproccessed_image = preproccess_image(im)
    #
    # cv2.imshow('out',preproccessed_image)
    # cv2.waitKey(0)
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(1,1),0)
    # blur = gray
    threshold = 140
    _, preproccessed_image = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)

    cv2.imshow('out',preproccessed_image)
    cv2.waitKey(0)

    contours,hierarchy = cv2.findContours(preproccessed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    out = np.zeros(im.shape, np.uint8)
    digits = []

    for cnt in contours:
        if cv2.contourArea(cnt)>0:
            [x,y,w,h] = cv2.boundingRect(cnt)
            if  (h>14 and h<18 and w<14) or (h>0 and h<5 and w<5):
            # if (h > 14 and h < 18 and w < 14) or (h > 0 and h < 5 and w < 5):
            # if 1==1:
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
    print('result_number = ', result_number)
    result_number = float(result_number)


    cv2.imshow('im',im)
    # cv2.imwrite('data/im.png', im)
    cv2.imshow('out',out)
    cv2.waitKey(0)

    return result_number

# get_number(r'D:\Development\PyCharm\rlcard\screenshots/screen_digits_3_PIL.png')
get_number(r'D:\Development\PyCharm\rlcard\gamereader/bet_screen_CV4.png')