from pandas_datareader import data as pdr
import fix_yahoo_finance as yf

yf.pdr_override()
startTime = "2017-10-01"
endTime = "2018-10-01"


def getsDataFromYahooFinance(company):
    data = None
    try:
        data = pdr.get_data_yahoo(company, start=startTime, end=endTime)
        # 輸出成 csv 方便自己查看
        data.to_csv('.\\output\\' + company + '.csv')
    except:
        print('Something Error, Please Try Again!')
    return data


def getVIX(company):
    print('VIX Not Yet!')


def calculateVolatility(data):
    print('Volatility Not Yet!')


def getDataAndCalculate(company):
    companyData = getsDataFromYahooFinance(company)
    calculateVolatility(companyData)


# 從這開始看
# 填入公司名字
getDataAndCalculate('AAPL')
getDataAndCalculate('GOOG')
getDataAndCalculate('AMZN')
