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
driver.get("https://www.marketwatch.com/games/svsc-x-fia")

try:
    annoyingPopup = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/footer/div[2]/div/div/button"))
    )
    annoyingPopup.click()
finally:

    join_game_button = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[5]/div[1]/div/div[3]/button"))
    )
    join_game_button_size = join_game_button.size
    h = join_game_button_size['height']
    driver.execute_script("arguments[0].scrollIntoView();", join_game_button)
    driver.execute_script("window.scrollBy(0, arguments[0]);", h*-1)
    join_game_button.click()

time.sleep(0.5)

email_box = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))
)
email_box.send_keys('lizardshipeve@gmail.com')
email_box.send_keys(Keys.ENTER)


password_box = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="password-login-password"]'))
)

with open('PASSWORD.txt') as f:
    password = f.readlines()
password_box.send_keys(password)
password_box.send_keys(Keys.ENTER)

ticker = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[5]/div[1]/div[1]/div/div[1]/input'))
)
#ticker_text_size = ticker.size
#ticker_text_height = ticker_text_size['height']
#driver.execute_script("arguments[0].scrollIntoView();", ticker)
#driver.execute_script("window.scrollBy(0, arguments[0]);", ticker_text_height*-1)

ticker.send_keys('SPY')
ticker.send_keys(Keys.ENTER)

trade_button = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[5]/div[1]/div[1]/div/div[2]/table/tbody/tr[1]/td[4]/button'))
)
trade_button_size = trade_button.size
h = trade_button_size['height']
driver.execute_script("arguments[0].scrollIntoView();", trade_button)
driver.execute_script("window.scrollBy(0, arguments[0]);", h*-1)
trade_button.click()



stock_slider = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div/div[1]/form/div[2]/div[2]/div[3]/input'))
)

move = ActionChains(driver)
try:
    move.click_and_hold(stock_slider).move_by_offset(1,0).release().perform()
    time.sleep(0.1)
finally:
    random = 0


submit_order = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div/div[1]/form/div[3]/div/button[3]'))
)
submit_order.click()


exit_submit_order = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div/div[2]/div/div/button'))
)
exit_submit_order.click()





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
        if left == True: #BUY FOR AFTER HOURS
            goto_portfolio = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[2]/div[2]/div/a[2]'))
            )
            goto_portfolio.click()


            pending_orders = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[5]/div[1]/div[6]/mw-tabs/div[1]/ul/button[2]'))
            )

            pending_button_size = pending_orders.size
            h = pending_button_size['height']
            driver.execute_script("arguments[0].scrollIntoView();", pending_orders)
            driver.execute_script("window.scrollBy(0, arguments[0]);", h*-1)

            pending_orders.click()


            cancel_order = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[5]/div[1]/div[6]/mw-tabs/div[2]/div[2]/div/table/tbody/tr/td[5]/div/button/span'))
            )
            cancel_order.click()
            confirm_cancel = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[5]/div[1]/div[6]/mw-tabs/div[2]/div[2]/div/div/div/div/div/div/div/button[1]'))
            )
            confirm_cancel.click()
            ticker = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[5]/div[1]/div[1]/div/div[1]/input'))
            )


            ticker.send_keys('SPY')

            time.sleep(0.5)
            
            ticker.send_keys(Keys.ENTER)

            trade_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[5]/div[1]/div[1]/div/div[2]/table/tbody/tr[1]/td[4]/button'))
            )
            trade_button_size = trade_button.size
            h = trade_button_size['height']
            driver.execute_script("arguments[0].scrollIntoView();", trade_button)
            driver.execute_script("window.scrollBy(0, arguments[0]);", h*-1)
            trade_button.click()

            stock_slider = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div/div[1]/form/div[2]/div[2]/div[3]/input'))
            )

            move = ActionChains(driver)
            try:
                move.click_and_hold(stock_slider).move_by_offset(1,0).release().perform()
                time.sleep(0.1)
            finally:
                random = 0


            submit_order = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div/div[1]/form/div[3]/div/button[3]'))
            )
            submit_order.click()


            exit_submit_order = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div/div[2]/div/div/button'))
            )
            exit_submit_order.click()

        else: #SHORT FOR AFTER HOURS
            goto_portfolio = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[2]/div[2]/div/a[2]'))
            )
            goto_portfolio.click()


            pending_orders = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[5]/div[1]/div[6]/mw-tabs/div[1]/ul/button[2]'))
            )

            pending_button_size = pending_orders.size
            h = pending_button_size['height']
            driver.execute_script("arguments[0].scrollIntoView();", pending_orders)
            driver.execute_script("window.scrollBy(0, arguments[0]);", h*-1)

            pending_orders.click()


            cancel_order = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[5]/div[1]/div[6]/mw-tabs/div[2]/div[2]/div/table/tbody/tr/td[5]/div/button/span'))
            )
            cancel_order.click()
            confirm_cancel = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[5]/div[1]/div[6]/mw-tabs/div[2]/div[2]/div/div/div/div/div/div/div/button[1]'))
            )
            confirm_cancel.click()



            ticker = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[5]/div[1]/div[1]/div/div[1]/input'))
            )
            ticker.send_keys('SPY')

            time.sleep(0.5)

            ticker.send_keys(Keys.ENTER)

            trade_button = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div[5]/div[1]/div[1]/div/div[2]/table/tbody/tr[1]/td[4]/button'))
            )
            trade_button_size = trade_button.size
            h = trade_button_size['height']
            driver.execute_script("arguments[0].scrollIntoView();", trade_button)
            driver.execute_script("window.scrollBy(0, arguments[0]);", h*-1)
            trade_button.click()

            sell_short = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div/div[1]/form/div[1]/ul/li[2]/label'))
            )
            sell_short.click()
            stock_slider = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div/div[1]/form/div[2]/div[2]/div[3]/input'))
            )

            move = ActionChains(driver)
            try:
                move.click_and_hold(stock_slider).move_by_offset(1,0).release().perform()
                time.sleep(0.1)
            finally:
                random = 0


            submit_order = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div/div[1]/form/div[3]/div/button[3]'))
            )
            submit_order.click()


            exit_submit_order = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[7]/div/div/div[2]/div/div/button'))
            )
            exit_submit_order.click()

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([frame, mask])

    cv2.imshow('Horizontal Stacking', hStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
cap.release()
cv2.destroyAllWindows()