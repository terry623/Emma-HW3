import datetime
from pandas_datareader import data as pdr

start = datetime.datetime(2016, 10, 1)
end = datetime.datetime(2018, 10, 1)


def getsDataFromYahooFinance(company):
    data = None

    try:
        data = pdr.DataReader('AAPL', 'yahoo', start, end)
        # 也會輸出成 csv 方便自己查看
        data.to_csv('.\\output\\' + company + '.csv')
    except:
        print('Something Error, Please Try Again!')

    return data


def getVIX(company):
    print('-----\nVIX Not Yet!')


def calculateVolatility(data):
    print('-----\nVolatility Not Yet!')


def getDataAndCalculate(company):
    companyData = getsDataFromYahooFinance(company)
    # calculateVolatility(companyData)


# 從這開始看
# 填入公司名字
getDataAndCalculate('AAPL')
getDataAndCalculate('GOOG')
getDataAndCalculate('AMZN')
print('\nFINISH !!')
