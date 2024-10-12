import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

os.environ['PATH'] += r"C:/SeleniumDrivers"
driver = webdriver.Firefox()
driver.get("https://www.marketwatch.com/games/svsc-x-fia")