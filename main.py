from pandas_datareader import data as pdr
import fix_yahoo_finance as yf

yf.pdr_override()
startTime = "2017-10-01"
endTime = "2018-10-01"


def getsDataFromYahooFinance(company):
    try:
        data = pdr.get_data_yahoo(company, start=startTime, end=endTime)
        data.to_csv('.\\output\\' + company + '.csv')
    except:
        print('Something Error, Please Try Again!')


def getVIX(company):
    print('VIX Not Yet!')


def calculateVolatility():
    print('Volatility Not Yet!')


getsDataFromYahooFinance("AAPL")
