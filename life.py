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
line_notify_token = LineConfig.LINE_NOTIFY_TOKEN
# line_notify_token = LineConfig.LINE_NOTIFY_TOKEN_TEST
line_notify_api = "https://notify-api.line.me/api/notify"
life_addr = "http://www.lifecorp.jp/store/syuto/855.html"

def LifeMessage():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "download.default_directory": "/home/pi6433162/Documents/Line",
        "plugins.always_open_pdf_externally": True
    })
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options, executable_path=CHROME_DRIVER)
    browser.get(life_addr)
    elm = browser.find_elements_by_class_name('shufoo-text')
    if len(elm) != 0:
        message = elm[0].text
    with open("/home/pi6433162/Documents/Line/life.txt", mode='r') as f:
        yesterday = f.read()
    with open("/home/pi6433162/Documents/Line/life.txt", mode='w') as f:
        f.write(message)
    if (len(elm) != 0) and (yesterday != message):
        os.system("rm -f /home/pi6433162/Documents/Line/chirashi.pdf")
        os.system("rm -f /home/pi6433162/Documents/Line/chirashi-1.png")
        os.system("rm -f /home/pi6433162/Documents/Line/chirashi-2.png")
        sleep(3)
        href = browser.find_elements_by_class_name('shufoo-pdf')[0].\
                       find_elements_by_tag_name('a')[0].get_attribute("href")
        browser.get(href)
        sleep(7)
        os.system("pdftoppm /home/pi6433162/Documents/Line/chirashi.pdf -png /home/pi6433162/Documents/Line/chirashi")
        sleep(7)

        message = "【Life 更新】" + message
        # message = message + "http://www.lifecorp.jp/store/syuto/855.html\n"
        if os.path.exists("/home/pi6433162/Documents/Line/chirashi-1.png"):
            payload = {"message":message + "(1)"}  #メッセージの本文
            headers = {"Authorization":"Bearer " + line_notify_token}
            files = {"imageFile":open("/home/pi6433162/Documents/Line/chirashi-1.png","rb")}
            line_notify = requests.post(line_notify_api, data = payload, headers = headers, files=files)

        if os.path.exists("/home/pi6433162/Documents/Line/chirashi-2.png"):
            payload = {"message":message + "(2)"}  #メッセージの本文
            files = {"imageFile":open("/home/pi6433162/Documents/Line/chirashi-2.png","rb")}
            line_notify = requests.post(line_notify_api, data = payload, headers = headers, files=files)
    else:
        message = "【Life 更新】本日はチラシがありません。"
        payload = {"message": message}  #メッセージの本文
        headers = {"Authorization":"Bearer " + line_notify_token}
        line_notify = requests.post(line_notify_api, data = payload, headers = headers)
    browser.quit

if __name__ == "__main__":
    LifeMessage()
    # test()
    print("Successful")
