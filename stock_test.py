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

    txe = Transaction({'Date': datetime.date(2015, 1, 1),
                       'Type': 'convert',
                       'NumShares': 99,
                       'MarketValue': 2})

    assert txe.date == datetime.date(2015, 1, 1)
    assert txe.type == Transaction.convert
    assert txe.numShares == 99
    assert txe.marketValue == 2


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
  def rate(self):
    return {'TTB': 1, 'TTM': 2, 'TTS': 3}

  def testCreate(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'buy',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = PurchaseReport(tx, self.rate(), 'USD')
    assert report.transaction is tx
    assert report.rate['TTB'] == 1
    assert report.rate['TTM'] == 2
    assert report.rate['TTS'] == 3
    assert report.currency == 'USD'

  def testEarnedIncomeInJPY(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'buy',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = PurchaseReport(tx, self.rate(), 'USD')
    assert report.earnedIncomeInJPY() == 96

  def testAcquisitionFeeInJPY(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'buy',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = PurchaseReport(tx, self.rate(), 'USD')
    assert report.acquisitionFeeInJPY() == 144

  def testTransferIncomeInJPY(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'buy',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = PurchaseReport(tx, self.rate(), 'USD')
    assert report.transferIncomeInJPY() == 0

  def testNumSharesDiff(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'buy',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = PurchaseReport(tx, self.rate(), 'USD')
    assert report.numSharesDiff() == 4

  def testToString(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'buy',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = PurchaseReport(tx, self.rate(), 'USD')
    s = str(report)
    assert s == ('2014-01-25: BUY 4 shares at 4 * 12.0 = USD48.0 = '
                 'JPY144.0 from JPY96.0 earnings.')


class TransferReportTest(TestCase):
  def testCreate(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'sell',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = TransferReport(tx, 5, 44, 'USD')
    assert report.transaction is tx
    assert report.ttb == 5
    assert report.currency == 'USD'

  def testEarnedIncomeInJPY(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'sell',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = TransferReport(tx, 5, 44, 'USD')
    assert report.earnedIncomeInJPY() == 0

  def testAcquisitionFeeInJPY(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'sell',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = TransferReport(tx, 5, 44, 'USD')
    assert report.acquisitionFeeInJPY() == 0

  def testTransferIncomeInJPY(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'sell',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = TransferReport(tx, 5, 44, 'USD')
    assert report.transferIncomeInJPY() == 64

  def testNumSharesDiff(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'sell',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = TransferReport(tx, 5, 44, 'USD')
    assert report.numSharesDiff() == -4

  def testToString(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'sell',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = TransferReport(tx, 5, 44, 'USD')
    s = str(report)
    assert (s == '2014-01-25: SELL 4 shares at 4 * 12.0 = USD48.0 = '
                 'JPY240.0. The purchase price per share is JPY44 and the '
                 'transfer income is JPY64.0.')
    assert report.transferIncomeInJPY() == 64


class ConvertReportTest(TestCase):
  def testCreate(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'convert',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = ConvertReport(tx, 5, 44, 'USD')
    assert report.transaction is tx
    assert report.ttb == 5
    assert report.currency == 'USD'

  def testEarnedIncomeInJPY(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'convert',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = ConvertReport(tx, 5, 44, 'USD')
    assert report.earnedIncomeInJPY() == 0

  def testAcquisitionFeeInJPY(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'convert',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = ConvertReport(tx, 5, 44, 'USD')
    assert report.acquisitionFeeInJPY() == 0

  def testTransferIncomeInJPY(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'convert',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = ConvertReport(tx, 5, 44, 'USD')
    assert report.transferIncomeInJPY() == 64

  def testNumSharesDiff(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'convert',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = ConvertReport(tx, 5, 44, 'USD')
    assert report.numSharesDiff() == 0

  def testToString(self):
    tx = Transaction({'Date': datetime.date(2014, 1, 25),
                      'Type': 'convert',
                      'NumShares': 4,
                      'MarketValue': 12})
    report = ConvertReport(tx, 5, 44, 'USD')
    s = str(report)
    assert (s == '2014-01-25: CONVERT 4 shares at 4 * 12.0 = USD48.0 = '
                 'JPY240.0. The purchase price per share is JPY44 and the '
                 'transfer income is JPY64.0.')
    assert report.transferIncomeInJPY() == 64


class IntegrationTest(TestCase):
  def testReports(self):
    class FakeExchanger:
      def rate(self, src, dest, d):
        if d == date(2013, 1, 4):
          return {'TTB': 20, 'TTM': 25, 'TTS': 30}
        if d == date(2013, 1, 10):
          return {'TTB': 20, 'TTM': 25, 'TTS': 30}
        if d == date(2013, 2, 24):
          return {'TTB': 10, 'TTM': 15, 'TTS': 20}
        if d == date(2013, 4, 2):
          return {'TTB': 10, 'TTM': 15, 'TTS': 20}
        if d == date(2013, 9, 2):
          return {'TTB': 30, 'TTM': 35, 'TTS': 40}
        if d == date(2013, 12, 2):
          return {'TTB': 30, 'TTM': 35, 'TTS': 40}
        if d == date(2014, 2, 2):
          return {'TTB': 10, 'TTM': 15, 'TTS': 20}
        if d == date(2014, 3, 2):
          return {'TTB': 30, 'TTM': 35, 'TTS': 40}
        assert False

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
  - Date: 2013-12-02
    MarketValue: 15
    NumShares: 5
    Type: convert
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

    assert len(rs[2013]) == 6
    assert rs[2013][0].earnedIncomeInJPY() == 1250
    assert rs[2013][0].acquisitionFeeInJPY() == 1500
    assert rs[2013][0].transferIncomeInJPY() == 0
    assert rs[2013][1].earnedIncomeInJPY() == 300
    assert rs[2013][1].acquisitionFeeInJPY() == 360
    assert rs[2013][1].transferIncomeInJPY() == 0
    assert rs[2013][2].earnedIncomeInJPY() == 0
    assert rs[2013][2].acquisitionFeeInJPY() == 0
    assert rs[2013][2].transferIncomeInJPY() == -420
    assert rs[2013][3].earnedIncomeInJPY() == 0
    assert rs[2013][3].acquisitionFeeInJPY() == 0
    assert rs[2013][3].transferIncomeInJPY() == -220
    assert rs[2013][4].earnedIncomeInJPY() == 1575
    assert rs[2013][4].acquisitionFeeInJPY() == 1800
    assert rs[2013][4].transferIncomeInJPY() == 0
    assert rs[2013][5].earnedIncomeInJPY() == 0
    assert rs[2013][5].acquisitionFeeInJPY() == 0
    assert rs[2013][5].transferIncomeInJPY() == -170

    assert len(rs[2014]) == 2
    assert rs[2014][0].earnedIncomeInJPY() == 0
    assert rs[2014][0].acquisitionFeeInJPY() == 0
    assert rs[2014][0].transferIncomeInJPY() == -590
    assert rs[2014][1].earnedIncomeInJPY() == 630
    assert rs[2014][1].acquisitionFeeInJPY() == 720
    assert rs[2014][1].transferIncomeInJPY() == 0

  def testPWCCase(self):
    class FakeExchanger:
      def rate(self, src, dest, d):
        if d == date(2014, 7, 28):
          return {'TTB': -100000, 'TTM': 1, 'TTS': 102.79}
        if d == date(2015, 1, 23):
          return {'TTB': 117.53, 'TTM': 1, 'TTS': -100000}
        if d == date(2015, 1, 26):
          return {'TTB': -100000, 'TTM': 1, 'TTS': 118.67}
        if d == date(2015, 3, 25):
          return {'TTB': 118.82, 'TTM': 1, 'TTS': -100000}
        assert False

    input = '''\
Currency: USD
Transactions:
  - Date: 2014-07-28
    Type: buy
    NumShares: 30
    MarketValue: 588.63
  - Date: 2015-01-23
    Type: sell
    NumShares: 20
    MarketValue: 537.59
  - Date: 2015-01-26
    Type: buy
    NumShares: 60
    MarketValue: 534.34
  - Date: 2015-03-25
    Type: sell
    NumShares: 10
    MarketValue: 565.50
'''
    rs = reports(Transactions(yaml.load(input)), FakeExchanger())
    assert len(rs) == 2
    assert len(rs[2014]) == 1
    assert rs[2014][0].acquisitionFeeInJPY() == 1815159
    assert rs[2014][0].transferIncomeInJPY() == 0

    assert len(rs[2015]) == 3
    assert rs[2015][0].acquisitionFeeInJPY() == 0
    assert rs[2015][0].transferIncomeInJPY() == 53540  # Should be 53559?
    assert rs[2015][1].acquisitionFeeInJPY() == 3804608  # Shuold be 3804600?
    assert rs[2015][1].transferIncomeInJPY() == 0
    assert rs[2015][2].acquisitionFeeInJPY() == 0
    assert rs[2015][2].transferIncomeInJPY() == 41978  # Should be 41976?
