#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import requests
import os
import datetime
from bs4 import BeautifulSoup
import LineConfig

CHROME_BIN = "/usr/bin/chromium-browser"
CHROME_DRIVER = '/usr/bin/chromedriver'
# line_notify_token = LineConfig.LINE_NOTIFY_TOKEN
line_notify_token = LineConfig.LINE_NOTIFY_TOKEN_TEST
line_notify_api = "https://notify-api.line.me/api/notify"

headers = {
  "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}

dic = {
  "Color" : "https://www.amazon.co.jp/dp/B07WXL5YPW",
  "Black" : "https://www.amazon.co.jp/dp/B07WS7BZYF",
  "Animal" : "https://www.amazon.co.jp/dp/B084HPMVNN",
  # "Test" : "https://www.amazon.co.jp/dp/B07SR8MMSL",
}

line_str = "Amazon\n"

for key, url in dic.items():
  # print(url)
  r = requests.get(url, headers = headers)
  html = r.text
  soup = BeautifulSoup(html, 'html.parser')
  merchant = soup.find(id="merchant-info")
  if "Amazon.co.jp" in merchant.text:
    line_str += key + ": "
    line_str += url + "\n"
    line_str += str("Amazon.co.jp" in merchant.text) + "\n"
# print(line_str)

if "True" in line_str:
  payload = {"Message": line_str}  #メッセージの本文
  headers = {"Authorization":"Bearer " + line_notify_token}
  line_notify = requests.post(line_notify_api, data = payload, headers = headers)
