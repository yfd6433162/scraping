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
odakyu_addr = "https://www.odakyu.jp/cgi-bin/user/emg/emergency_bbs.pl"

def TrainMessage():
    # スクレイピング対象の URL にリクエストを送り HTML を取得する
    res = requests.get(odakyu_addr)

    # レスポンスの HTML から BeautifulSoup オブジェクトを作る
    soup = BeautifulSoup(res.text, 'html.parser')

    message = "【小田急 遅延情報】"
    message = message + "\n" + soup.find('p', {'class': 'date'}).get_text(strip=True)
    try:
        message_tmp = soup.find('p', {'class': 'ttl_daiya_blue'}).get_text(strip=True)
    except AttributeError:
        message_tmp = "ダイヤに乱れがあります。"
        message_tmp = message_tmp + soup.find('p', {'class': 'ttl_daiya'}).get_text(strip=True)
    message = message + "\n" + message_tmp

    payload = {"message":message}  #メッセージの本文
    headers = {"Authorization":"Bearer " + line_notify_token}
    line_notify = requests.post(line_notify_api, data = payload, headers = headers)

if __name__ == "__main__":
    TrainMessage()
    print("Successful")
