from pandas_datareader import data as pdr
import numpy as np
import datetime
import math

start = datetime.datetime(2018, 8, 1)
end = datetime.datetime(2018, 9, 30)
dateRange = 30
data = None


def getsDataFromYahooFinance(company):
    result = pdr.DataReader(company, 'yahoo', start, end)

    toCSV(result, company)
    drawChart(result, company)

    return result


def toCSV(result, company):
    # 輸出成 CSV 方便自己觀看
    result.to_csv('.\\output\\' + company + '.csv')


def drawChart(result, company):
    # 先畫除了 Volume 以外的 Column
    result.drop(columns=['Volume']).plot()


def getVIX(company):
    print('-----\nVIX Not Yet!')


def calculatePopulationMean():
    firstDay = data[0]
    lastDay = data[dateRange-1]
    differenceValue = abs(lastDay - firstDay)
    mean = math.log(differenceValue / firstDay) / dateRange

    return mean


def calculateSumSecond(day, mean):
    difference = data[day] - data[day-1]
    deltaTSquare = (1 / 365) ** 0.5
    result = (difference / (data[day] * deltaTSquare)
              - mean * deltaTSquare) ** 2

    return result


def calculateSum(mean):
    sumNum = 0
    for day in range(dateRange-1):
        sumNum += calculateSumSecond(day, mean)

    return sumNum


def calculateHistoricalVolatility(mean):
    historicalVolatility = (calculateSum(mean) / (dateRange - 1)) ** 0.5

    return historicalVolatility


# 還沒動態變成 30 天
def calculateVolatility(companyData, company):
    # sort dates in descending order
    companyData.sort_index(ascending=False, inplace=True)
    companyData.to_csv('.\\output\\' + company + '_TEST.csv')

    data = companyData['Close']
    populationMean = calculatePopulationMean()
    calculateHistoricalVolatility(populationMean)


def getDataAndCalculate(company):
    companyData = getsDataFromYahooFinance(company)
    calculateVolatility(companyData, company)


# 從這開始看
# 填入公司名字
getDataAndCalculate('AAPL')
print('\nFINISH !!')
