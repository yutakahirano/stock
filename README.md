```
$ cat example.yaml
Currency: USD
Transactions:
  - Date: 2013-02-04
    Type: buy
    NumShares: 4
    MarketValue: 221.42
  - Date: 2013-05-04
    Type: buy
    NumShares: 6
    MarketValue: 309.18
  - Date: 2013-06-08
    Type: sell
    NumShares: 4
    MarketValue: 101.42
  - Date: 2013-06-12
    Type: sell
    NumShares: 1
    MarketValue: 2309.18
  - Date: 2013-12-12
    Type: buy
    NumShares: 12
    MarketValue: 109.18
  - Date: 2014-02-12
    Type: sell
    NumShares: 5
    MarketValue: 309.18
  - Date: 2014-02-13
    Type: buy
    NumShares: 8
    MarketValue: 322.4
  - Date: 2014-05-13
    Type: buy
    NumShares: 4
    MarketValue: 422.4
$
$ python3
Python 3.4.3 (default, Oct 14 2015, 20:33:09)
[GCC 4.8.4] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import stock, mizuho
>>> ex = mizuho.MizuhoCurrencyRate()
>>> stock.report(stock.load('example.yaml'), ex)
===
2013-02-04: BUY 4 shares at 4 * 221.42 = USD885.68 = JPY82980.
2013-05-04: BUY 6 shares at 6 * 309.18 = USD1855.08 = JPY182206.
2013-06-08: SELL 4 shares at 4 * 101.42 = USD405.68 = JPY39123.7792. The purchase price per share is JPY26518.6 and the transfer income is JPY-66950.
2013-06-12: SELL 1 shares at 1 * 2309.18 = USD2309.18 = JPY220388.13919999998. The purchase price per share is JPY26518.5 and the transfer income is JPY193870.
2013-12-12: BUY 12 shares at 12 * 109.18 = USD1310.16 = JPY135838.
2013: The earned income is JPY401024.0, the transfer income is JPY126920.0.
2013: You have 17 shares at the end of year.
====
2014-02-12: SELL 5 shares at 5 * 309.18 = USD1545.9 = JPY156908.85. The purchase price per share is JPY15790.0 and the transfer income is JPY77959.
2014-02-13: BUY 8 shares at 8 * 322.4 = USD2579.2 = JPY266973.
2014-05-13: BUY 4 shares at 4 * 422.4 = USD1689.6 = JPY174384.
2014: The earned income is JPY441357.0, the transfer income is JPY77959.0.
2014: You have 24 shares at the end of year.
===
>>>
```
