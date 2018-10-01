from pandas_datareader import data as pdr
import datetime

start = datetime.datetime(2016, 10, 1)
end = datetime.datetime(2018, 10, 1)


def getsDataFromYahooFinance(company):
    data = pdr.DataReader(company, 'yahoo', start, end)

    toCSV(data, company)
    drawChart(data, company)

    return data


def toCSV(data, company):
    # 輸出成 CSV 方便自己觀看
    data.to_csv('.\\output\\' + company + '.csv')


def drawChart(data, company):
    # 先畫除了 Volume 以外的 Column
    data.drop(columns=['Volume']).plot()


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
