# -*- coding: utf-8 -*-
import unittest

from unittest import TestCase
from stock import *
from datetime import date

class TransactionTest(TestCase):
  def testCreate(self):
    txb = Transaction({'Date': datetime.date(2014, 1, 25),
                       'Type': 'buy',
                       'NumShares': '4',
                      'MarketValue': '12'})

    assert txb.date == datetime.date(2014, 1, 25)
    assert txb.type == Transaction.buy
    assert txb.numShares == 4
    assert txb.marketValue == 12

    txs = Transaction({'Date': datetime.date(2015, 1, 1),
                       'Type': 'sell',
                       'NumShares': 99,
                      'MarketValue': 2})

    assert txs.date == datetime.date(2015, 1, 1)
    assert txs.type == Transaction.sell
    assert txs.numShares == 99
    assert txs.marketValue == 2


class TransactionsTest(TestCase):
  def testCreate(self):
    input = {'Currency': 'USD', 'Transactions': [{
      'Date': datetime.date(2015, 2, 22),
      'Type': 'buy',
      'NumShares': '92',
      'MarketValue': '123'}, {
      'Date': datetime.date(2015, 3, 3),
      'Type': 'sell',
      'NumShares': '4',
      'MarketValue': '12'}]}
    txs = Transactions(input)
    assert txs.currency == 'USD'
    assert len(txs.transactions) == 2
    assert isinstance(txs.transactions[0], Transaction)
    assert isinstance(txs.transactions[1], Transaction)
    assert txs[0] is txs.transactions[0]
    assert txs[1] is txs.transactions[1]


class PurchaseReportTest(TestCase):
  def testCreate(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'buy',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = PurchaseReport(tx, 5, 'USD')
    assert report.transaction is tx
    assert report.ttm == 5
    assert report.currency == 'USD'

  def testEarnedIncomeInJPY(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'buy',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = PurchaseReport(tx, 5, 'USD')
    assert report.earnedIncomeInJPY() == 240

  def testTransferIncomeInJPY(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'buy',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = PurchaseReport(tx, 5, 'USD')
    assert report.transferIncomeInJPY() == 0

  def testToString(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'buy',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = PurchaseReport(tx, 5, 'USD')
    s = str(report)
    assert s == '2014-01-25: BUY 4 shares at 4 * 12.0 = USD48.0 = JPY240.0.'


class TransferReportTest(TestCase):
  def testCreate(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'sell',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = TransferReport(tx, 5, 44, 'USD')
    assert report.transaction is tx
    assert report.tts == 5
    assert report.currency == 'USD'

  def testEarnedIncomeInJPY(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'sell',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = TransferReport(tx, 5, 44, 'USD')
    assert report.earnedIncomeInJPY() == 0

  def testTransferIncomeInJPY(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'sell',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = TransferReport(tx, 5, 44, 'USD')
    assert report.transferIncomeInJPY() == 64

  def testToString(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'sell',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = TransferReport(tx, 5, 44, 'USD')
    s = str(report)
    assert (s == '2014-01-25: SELL 4 shares at 4 * 12.0 = USD48.0 = JPY240.0. '
      'The purchase price per share is JPY44 and the transfer income is '
      'JPY64.0.')
    assert report.transferIncomeInJPY() == 64

class FakeExchanger:
  def rate(self, src, dest, d):
    if d == date(2013, 1, 4):
      return {'TTM': 20, 'TTS': 30}
    if d == date(2013, 1, 10):
      return {'TTM': 20, 'TTS': 30}
    if d == date(2013, 2, 24):
      return {'TTM': 10, 'TTS': 20}
    if d == date(2013, 4, 2):
      return {'TTM': 10, 'TTS': 20}
    if d == date(2013, 9, 2):
      return {'TTM': 30, 'TTS': 40}
    if d == date(2014, 2, 2):
      return {'TTM': 10, 'TTS': 20}
    if d == date(2014, 3, 2):
      return {'TTM': 30, 'TTS': 40}
    assert False


class IntegrationTest(TestCase):
  def testReports(self):
    input = '''\
Currency: USD
Transactions:
  - Date: 2013-01-04
    MarketValue: 10
    NumShares: 5
    Type: buy
  - Date: 2013-01-10
    MarketValue: 12
    NumShares: 1
    Type: buy
  - Date: 2013-02-24
    MarketValue: 10
    NumShares: 2
    Type: sell
  - Date: 2013-04-02
    MarketValue: 20
    NumShares: 2
    Type: sell
  - Date: 2013-09-02
    MarketValue: 15
    NumShares: 3
    Type: buy
  - Date: 2014-02-02
    MarketValue: 1 
    NumShares: 1
    Type: sell
  - Date: 2014-03-02
    MarketValue: 18
    NumShares: 1
    Type: buy
'''
    rs = reports(Transactions(yaml.load(input)), FakeExchanger())
    assert len(rs) == 2
 
    assert len(rs[2013]) == 5
    assert rs[2013][0].earnedIncomeInJPY() == 1000
    assert rs[2013][0].transferIncomeInJPY() == 0
    assert rs[2013][1].earnedIncomeInJPY() == 240
    assert rs[2013][1].transferIncomeInJPY() == 0
    assert rs[2013][2].earnedIncomeInJPY() == 0
    assert rs[2013][2].transferIncomeInJPY() == -13
    assert rs[2013][3].earnedIncomeInJPY() == 0
    assert rs[2013][3].transferIncomeInJPY() == 387
    assert rs[2013][4].earnedIncomeInJPY() == 1350
    assert rs[2013][4].transferIncomeInJPY() == 0

    assert len(rs[2014]) == 2
    assert rs[2014][0].earnedIncomeInJPY() == 0
    assert rs[2014][0].transferIncomeInJPY() == -332
    assert rs[2014][1].earnedIncomeInJPY() == 540
    assert rs[2014][1].transferIncomeInJPY() == 0

