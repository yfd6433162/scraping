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

request_headers = {
  "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}

def AmazonChecker(dic):
  line_str = "Amazon\n"
  for key, url in dic.items():
    # print(url)
    r = requests.get(url, headers = request_headers)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    merchant = soup.find(id="merchant-info")
    if "Amazon.co.jp が販売" in merchant.text:
      line_str += key + ": "
      line_str += url + "\n"
      line_str += "在庫あり\n"
  # print(line_str)

  if "在庫あり" in line_str:
    payload = {"Message": line_str}  #メッセージの本文
    headers = {"Authorization":"Bearer " + line_notify_token}
    line_notify = requests.post(line_notify_api, data = payload, headers = headers)

def NintenAtsumoriChecker(dic):
  line_str = "Nintendo\n"
  for key, url in dic.items():
    r = requests.get(url, headers = request_headers)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find(class_="item-cart-add-area")
    try:
      if "カートに追加する" in str(item):
        line_str += key + ": "
        line_str += url + "\n"
        line_str += "在庫あり\n"
    except Exception as e:
      print(e)
  # print(line_str)

  if "在庫あり" in line_str:
    payload = {"Message": line_str}  #メッセージの本文
    headers = {"Authorization":"Bearer " + line_notify_token}
    line_notify = requests.post(line_notify_api, data = payload, headers = headers)

def NintenSwitchChecker(dic):
  line_str = "Nintendo\n"
  for key, url in dic.items():
    r = requests.get(url, headers = request_headers)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find(id="custoize_toCart")
    try:
      if not "準備中" in str(item):
        line_str += key + ": "
        line_str += url + "\n"
        line_str += "在庫あり\n"
    except Exception as e:
      print(e)
  # print(line_str)

  if "在庫あり" in line_str:
    payload = {"Message": line_str}  #メッセージの本文
    headers = {"Authorization":"Bearer " + line_notify_token}
    line_notify = requests.post(line_notify_api, data = payload, headers = headers)

def RakutenChecker(dic):
  line_str = "Rakuten\n"
  for key, url in dic.items():
    r = requests.get(url, headers = request_headers)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find(class_="status-heading")
    try:
      if not "ご注文できない商品" in str(item):
        line_str += key + ": "
        line_str += url + "\n"
        line_str += "在庫あり\n"
    except Exception as e:
      print(e)
  # print(line_str)

  if "在庫あり" in line_str:
    payload = {"Message": line_str}  #メッセージの本文
    headers = {"Authorization":"Bearer " + line_notify_token}
    line_notify = requests.post(line_notify_api, data = payload, headers = headers)

if __name__ == '__main__':
  dic = {
    "Color" : "https://www.amazon.co.jp/dp/B07WXL5YPW",
    "Black" : "https://www.amazon.co.jp/dp/B07WS7BZYF",
    "Animal" : "https://www.amazon.co.jp/dp/B084HPMVNN",
    "Ring" : "https://www.amazon.co.jp/dp/B0861F1JX1",
    # "Test" : "https://www.amazon.co.jp/dp/B07SR8MMSL",
  }
  AmazonChecker(dic)

  dic = {
    "Animal" : "https://store.nintendo.co.jp/item/HAD_S_KEAGC.html",
    "Ring" : "https://store.nintendo.co.jp/item/HAC_R_AL3PA.html",
    "Ring_Download" : "https://store.nintendo.co.jp/item/HAC_Q_AL3PA.html",
    # "Test" : "https://store.nintendo.co.jp/item/HAC_J_AUBQACF1.html",
  }
  NintenAtsumoriChecker(dic)

  dic = {
    "Custom" : "https://store.nintendo.co.jp/item/HAD_S_KAYAA.html",
    "2daime" : "https://store.nintendo.co.jp/item/HAD_9_KAZAB.html",
  }
  NintenSwitchChecker(dic)

  dic = {
    # "Test" : "https://books.rakuten.co.jp/rb/14647226/",
    "Color" : "https://books.rakuten.co.jp/rb/16033028/",
    "Black" : "https://books.rakuten.co.jp/rb/16033027/",
    "Animal" : "https://books.rakuten.co.jp/rb/16247994/",
    "Ring" : "https://books.rakuten.co.jp/rb/16057071/",
  }
  RakutenChecker(dic)
