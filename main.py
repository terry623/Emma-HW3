import time
from pandas_datareader import data as pdr
from requests_html import HTMLSession
session = HTMLSession()


def convertTime(target):
    st = time.strptime(target, '%Y-%m-%d')
    return str(int(time.mktime(st)))


def getsDataFromYahooFinance(company, start, end):
    url = 'https://finance.yahoo.com/quote/' + company + \
        '/history?period1=' + \
        convertTime(start) + \
        '&period2=' + convertTime(end) + \
        '&interval=1d&filter=history&frequency=1d'
    data = None

    try:
        response = session.get(url)
        select = '#Col1-1-HistoricalDataTable-Proxy > section > div:nth-child(2)> table > tbody'
        table = response.html.find(select, first=True)
        data = table.text
    except:
        print('Something Error, Please Try Again!')

    return data


def getVIX(company):
    print('-----\nVIX Not Yet!')


def calculateVolatility(data):
    print('-----\nVolatility Not Yet!')


def getDataAndCalculate(company, start, end):
    companyData = getsDataFromYahooFinance(company, start, end)
    print(companyData)
    # calculateVolatility(companyData)


# 填入公司名字、起始時間、結束時間
getDataAndCalculate('AAPL', '2018-07-01', '2018-9-01')
