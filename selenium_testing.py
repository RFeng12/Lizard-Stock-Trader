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




os.environ['PATH'] += r"C:/SeleniumDrivers"
driver = webdriver.Firefox()
driver.get("http://rfeng.pythonanywhere.com/")
while True:
    driver.refresh()

