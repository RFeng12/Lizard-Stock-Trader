# import the opencv library
import cv2
import numpy as np  
from enum import Enum
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
import time

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0)

cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
    pass

cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640,240)
cv2.createTrackbar("HUE Min", "HSV", 9, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 23, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 15, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 214, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 150, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 212, 255, empty)


left = True

first = True

#prev = np.array([],[])


while(True):
    ret, frame = cap.read()
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frameRGB = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2RGB)


    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(frameHSV, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask = mask)

    resultRGB = cv2.cvtColor(src=result, code=cv2.COLOR_BGR2RGB)
    prepared_frame = cv2.cvtColor(resultRGB, cv2.COLOR_BGR2GRAY)
    prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5,5), sigmaX=0)

    if first == True:
        motion = mask
        
    else:
        motion = cv2.absdiff(src1=prev, src2=prepared_frame)        



#    leftsum = 0
#    rightsum = 0

#    for i in range (0, 480):
#        for j in range(0, 320):
#            leftsum = leftsum + mask[i][j]/255
#        for j in range(320, 640):
#            rightsum = rightsum + mask[i][j]/255

 #   temp = left

#    if rightsum > leftsum:
#        left = False
#    else:
#        left = True

    prev = prepared_frame




    #mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  #for converting mask to same dimensions as other frames
    #hStack = np.hstack([frame, mask])
    
    unalteredmotion = motion

    #kernel = np.ones((5, 5))
    #motion = cv2.dilate(motion, kernel, 1) # could be useless/detrimental
    
    unalteredmotion = cv2.threshold(src=unalteredmotion, thresh=80, maxval=255, type=cv2.THRESH_BINARY)[1] #could be useless/detrimental



    splitted = np.hsplit(unalteredmotion, 2)

    sumleft = np.sum(splitted[0])
    sumright = np.sum(splitted[1])

    print(sumright)
    print(sumleft)

    if sumleft > sumright*1.5:
        print('left')

    elif sumright > sumleft*1.5:
        print("right")
    
    else: 
        print("ambiguous")

    hStack = np.hstack([unalteredmotion])
    cv2.imshow('Horizontal Stacking', hStack)

    first = False

    


    time.sleep(0.1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
cap.release()
cv2.destroyAllWindows()