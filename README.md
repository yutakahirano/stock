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
2013-02-04: BUY 4 shares at 4 * 221.42 = USD885.68 = JPY81208.
2013-05-04: BUY 6 shares at 6 * 309.18 = USD1855.08 = JPY178496.
2013-06-08: SELL 4 shares at 4 * 101.42 = USD405.68 = JPY39935.1392. The purchase price per share is JPY25970.4 and the transfer income is JPY-63946.
2013-06-12: SELL 1 shares at 1 * 2309.18 = USD2309.18 = JPY225006.4992. The purchase price per share is JPY25970.333333333332 and the transfer income is JPY199037.
2013-12-12: BUY 12 shares at 12 * 109.18 = USD1310.16 = JPY133218.
2013: The earned income is JPY392922.0, the transfer income is JPY135091.0.
====
2014-02-12: SELL 5 shares at 5 * 309.18 = USD1545.9 = JPY160000.65000000002. The purchase price per share is JPY15474.64705882353 and the transfer income is JPY82628.
2014-02-13: BUY 8 shares at 8 * 322.4 = USD2579.2 = JPY261815.
2014-05-13: BUY 4 shares at 4 * 422.4 = USD1689.6 = JPY171005.
2014: The earned income is JPY432820.0, the transfer income is JPY82628.0.
====
>>>
```
