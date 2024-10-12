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
cv2.createTrackbar("SAT Min", "HSV", 34, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 214, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 150, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 212, 255, empty)


left = True

while(True):
    ret, frame = cap.read()
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

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

    leftsum = 0
    rightsum = 0

    for i in range (0, 480):
        for j in range(0, 320):
            leftsum = leftsum + mask[i][j]/255
        for j in range(320, 640):
            rightsum = rightsum + mask[i][j]/255

    temp = left

    if rightsum > leftsum:
        left = False
    else:
        left = True
    if temp != left:
        if left == True: #BUY 
            print("buy")
            

        else: #SHORT FOR AFTER HOURS
           print("shhort")

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    #hStack = np.hstack([frame, mask])
    hStack = np.hstack([ mask])
    cv2.imshow('Horizontal Stacking', hStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
cap.release()
cv2.destroyAllWindows()