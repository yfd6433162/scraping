#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import datetime
import os
from bs4 import BeautifulSoup
import LineConfig

CHROME_BIN = "/usr/bin/chromium-browser"
CHROME_DRIVER = '/usr/bin/chromedriver'
# line_notify_token = LineConfig.LINE_NOTIFY_TOKEN
line_notify_token = LineConfig.LINE_NOTIFY_TOKEN_TEST
line_notify_api = "https://notify-api.line.me/api/notify"
weather_addr = "https://tenki.jp/forecast/3/17/"

def WeatherMessage():
    options = Options()
    options.binary_location = CHROME_BIN
    options.add_argument('--headless')
    driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=options)
    driver.get(weather_addr)
    w = 750
    h = 900
    driver.set_window_size(w,h)
    png = driver.find_elements_by_xpath('/html/body/div[2]/section/div[1]/img')[0].screenshot_as_png
    driver.quit

    res = requests.get(weather_addr)
    soup = BeautifulSoup(res.text, 'html.parser')

    dt_now = datetime.datetime.now()
    message = "【神奈川 天気情報】"
    # message = message + "\n" + dt_now.strftime('%Y/%m/%d %H:%M')
    # message = message + "\n" + soup.find('div', {'class': 'forecast-comment'}).get_text(strip=True)

    payload = {"message":message}  #メッセージの本文
    headers = {"Authorization":"Bearer " + line_notify_token}
    files = {"imageFile":png} #画像も送れる(jpegとpng対応)
    line_notify = requests.post(line_notify_api, data = payload, headers = headers, files = files)

if __name__ == "__main__":
    WeatherMessage()
    # test()
    print("Successful")
