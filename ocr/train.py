import cv2
import numpy as np

#######   training part    ###############
samples = np.loadtxt('data/generalsamples.data',np.float32)
responses = np.loadtxt('data/generalresponses.data',np.float32)
responses = responses.reshape((responses.size,1))

model = cv2.ml.KNearest_create()
model.train(samples,cv2.ml.ROW_SAMPLE, responses)

model.save("model/model.xml")
# model.load("model/model.dat")


############################# testing part  #########################

im = cv2.imread(r'D:\Development\PyCharm\simple-ocr-opencv\simpleocr\data\2.png')
out = np.zeros(im.shape,np.uint8)


gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(3,3),0)
threshold = 100
_, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


# gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
# thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)

# contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

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
            print('string = ', string)
            cv2.putText(out,string,(x,y+h),0,1,(0,255,0))


        elif  h>0 and h<5 and w<5 and 1==5:
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
            roi = thresh[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(10,10))
            roismall = roismall.reshape((1,100))
            roismall = np.float32(roismall)
            retval, results, neigh_resp, dists = model.findNearest(roismall, k = 1)
            string = str(chr(results[0][0]))
            print('string = ', string)
            cv2.putText(out,string,(x,y+h),0,1,(0,255,0))

cv2.imshow('im',im)
cv2.imshow('out',out)
cv2.waitKey(0)