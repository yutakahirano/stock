#
# -*- coding: utf-8 -*-
import yaml
import datetime
import re
import math
import mizuho


class Transaction:
  sell = object()
  buy = object()

  def __init__(self, dict):
    self.date = dict['Date']
    assert type(self.date) is datetime.date
    if dict['Type'] == 'sell':
      self.type = Transaction.sell
    else:
      assert dict['Type'] == 'buy'
      self.type = Transaction.buy
    self.numShares = int(dict['NumShares'])
    self.marketValue = float(dict['MarketValue'])


class Transactions:
  def __init__(self, data):
    self.currency = data['Currency']
    assert(data['Currency'] == 'USD')
    self.transactions = [Transaction(i) for i in data['Transactions']]

  def __iter__(self):
    return self.transactions.__iter__()

  def __getitem__(self, *args):
    return self.transactions.__getitem__(*args)


class PurchaseReport:
  def __init__(self, transaction, ttm, currency):
    self.transaction = transaction
    self.ttm = ttm
    self.currency = currency

  def __str__(self):
    return '{0}: BUY {1} shares at {1} * {2} = {3}{4} = JPY{5}.'.format(
      self.transaction.date,
      self.transaction.numShares,
      self.transaction.marketValue,
      self.currency,
      self.transaction.numShares * self.transaction.marketValue,
      self.valueInJPY())

  def valueInJPY(self):
    tx = self.transaction
    return math.ceil(tx.numShares * tx.marketValue * self.ttm)

  def earnedIncomeInJPY(self):
    return self.valueInJPY()

  def transferIncomeInJPY(self):
    return 0.0

  def numSharesDiff(self):
    return self.transaction.numShares


class TransferReport:
  def __init__(self, transaction, tts, purchasePricePerShare, currency):
    self.transaction = transaction
    self.tts = tts
    self.currency = currency
    self.purchasePricePerShareInJPY = purchasePricePerShare

  def __str__(self):
    tx = self.transaction
    return ('{0}: SELL {1} shares at {1} * {2} = {3}{4} = JPY{5}. The '
            'purchase price per share is JPY{6} and the transfer income '
            'is JPY{7}.'.format(tx.date,
                                tx.numShares,
                                tx.marketValue,
                                self.currency,
                                tx.numShares * tx.marketValue,
                                tx.numShares * tx.marketValue * self.tts,
                                self.purchasePricePerShareInJPY,
                                self.transferIncomeInJPY()))

  def earnedIncomeInJPY(self):
    return 0.0

  def transferIncomeInJPY(self):
    tx = self.transaction
    purchasePrice = tx.numShares * self.purchasePricePerShareInJPY
    return math.ceil(tx.numShares * tx.marketValue * self.tts - purchasePrice)

  def numSharesDiff(self):
    return -self.transaction.numShares


def load(filename):
  with open(filename, 'r') as f:
    data = yaml.safe_load(f)
  return Transactions(data)


def reports(transactions, exchanger):
  currency = transactions.currency

  numShares = 0
  totalValue = 0.0

  reports = {}

  for tx in sorted(transactions, key=lambda x: x.date):
    if tx.date.year not in reports:
      reports[tx.date.year] = []

    rate = exchanger.rate(currency, 'JPY', tx.date)
    ttm = rate['TTM']
    tts = rate['TTS']

    average = totalValue / numShares if numShares > 0 else 0.0
    if tx.type is Transaction.buy:
       reports[tx.date.year].append(PurchaseReport(tx, ttm, currency))

       numShares += tx.numShares
       totalValue += math.ceil(tx.numShares * tx.marketValue * ttm)
    else:
       assert tx.type is Transaction.sell
       reports[tx.date.year].append(TransferReport(tx, tts, average, currency))

       numShares -= tx.numShares
       totalValue -= math.ceil(tx.numShares * average)
  return reports


def report(transactions, exchanger):
  print('===')
  numShares = 0
  for year, xs in sorted(reports(transactions, exchanger).items()):
    earnedIncomeInJPY = 0
    transferIncomeInJPY = 0
    for report in xs:
      print(report)
      earnedIncomeInJPY += report.earnedIncomeInJPY()
      transferIncomeInJPY += report.transferIncomeInJPY()
      numShares += report.numSharesDiff()

    print('{0}: The earned income is JPY{1}, the transfer income is JPY{2}.'
          .format(year, earnedIncomeInJPY, transferIncomeInJPY))
    print('{0}: You have {1} shares at the end of year.'.format(
      year, numShares))
    print('====')
