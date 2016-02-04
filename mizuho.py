# -*- coding: utf-8 -*-
import datetime
import requests
import re

class MizuhoCurrencyRate:
  def __init__(self):
    self.cache = {}

  # Returns the price of the unit of |src| currency in |dest| currency at a
  # certain time. The return value is a pair consisting of TTB and TTS.
  # Example: If 1 USD = 111.5 JPY (TTS) and 110.5 JPY(TTB), return
  # {'TTB': 110.5, 'TTS': 111.5}
  def rate(self, src, dest, date):
    key = (src, dest, date)
    if key in self.cache:
      return self.cache[key]

    assert src == 'USD'
    assert dest == 'JPY'
    urlPattern = \
      'https://www.mizuhobank.co.jp/rate/market/quote/data/quote_{0}.txt'
    while True:
      url = urlPattern.format(date.strftime('%Y%m%d'))
      response = requests.get(url)
      if response.status_code == 404:
        date = date - datetime.timedelta(days=1)
        continue

      assert response.status_code == 200
      # Unfortunately, the server doesn't return the correct encoding.
      response.encoding = 'SHIFT-JIS'
      for line in response.text.split('\n'):
        pattern = re.compile(r'^米ドル +USD +(\d+\.\d*) +(\d+\.\d*) +\d+\.\d*')
        m = pattern.match(line)
        if m:
          value = {'TTS': float(m.group(1)), 'TTB': float(m.group(2))}
          self.cache[key] = value
          return value
      assert False, 'Should never reach.'
    return
