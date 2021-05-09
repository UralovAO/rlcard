import cv2
import numpy as np

def get_number(image_path = 'data/2.png'):

    model = cv2.ml.KNearest_load("model/model.xml")

    im = cv2.imread(image_path)


    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(3,3),0)
    threshold = 100
    _, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    out = np.zeros(im.shape, np.uint8)
    digits = []

    for cnt in contours:
        if cv2.contourArea(cnt)>0:
            [x,y,w,h] = cv2.boundingRect(cnt)
            if  (h>14 and h<18 and w<14) or (h>0 and h<5 and w<5):
                cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                roi = thresh[y:y+h,x:x+w]
                roismall = cv2.resize(roi,(10,10))
                roismall = roismall.reshape((1,100))
                roismall = np.float32(roismall)
                retval, results, neigh_resp, dists = model.findNearest(roismall, k = 1)
                string = str(chr(results[0][0]))
                digits.append((x, string))
                # print('string = ', string)
                cv2.putText(out,string,(x,y+h),0,1,(0,255,0))
    digits = sorted(digits)
    print('digits = ', digits)
    result_number = [x[1] for x in digits]
    result_number = "".join(result_number)
    result_number = float(result_number)
    print(result_number)

    cv2.imshow('im',im)
    cv2.imshow('out',out)
    cv2.waitKey(0)