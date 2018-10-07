from pandas_datareader import data as pdr
import pandas as pd
import numpy as np
import datetime
import csv
import math

allDataStart = datetime.datetime(2016, 10, 1)
allDataEnd = datetime.datetime(2018, 10, 1)
dateRange = 30
numberOfTimes = 500 - dateRange + 1


def drawChart(result, company):
    title = company + ' ( ' + str(dateRange) + ' days' + ' )'
    figure = result.plot(x="startDay", y='volatility', title=title)
    figure.set(xlabel='Number of Times')


def getVIX(company):
    print('VIX Not Yet!')


def calculatePopulationMean(data, start, end):
    firstDay = data[start]
    lastDay = data[end]
    differenceValue = abs(lastDay - firstDay)
    mean = math.log(differenceValue / firstDay) / dateRange

    return mean


def totalSum(data, mean, start, end):
    sumNum = 0

    for day in range(start, end):
        difference = data[day] - data[day-1]
        deltaTSquare = (1 / 365) ** 0.5
        result = (difference / (data[day] * deltaTSquare)
                  - mean * deltaTSquare) ** 2
        sumNum += result

    return sumNum


def calculateVolatility(data, mean, start, end):
    historicalVolatility = (
        totalSum(data, mean, start, end) / (dateRange - 1)) ** 0.5

    return historicalVolatility


def calculateAndDraw(companyData, company):
    companyData.sort_index(ascending=False, inplace=True)
    companyData.to_csv('.\\EXCEL\\' + company + '\\' + company + '.csv')
    data = companyData['Close']

    result = pd.DataFrame(columns=['startDay', 'endDay', 'volatility'])

    # 從第二個開始算，因為要看前一天去算差值
    for start in range(1, numberOfTimes + 1):
        end = start + dateRange - 1
        populationMean = calculatePopulationMean(data, start, end)
        historicalVolatility = calculateVolatility(
            data, populationMean, start, end)

        print('startDay:', start, ", endDay:", end,
              ', volatility:', historicalVolatility)

        result = result.append({'startDay': start, 'endDay': end,
                                'volatility': historicalVolatility}, ignore_index=True)
    result.to_csv('.\\EXCEL\\' + company + '\\' + company + '_Result.csv')
    # drawChart(result, company)


def getDataAndCalculate(company):
    companyData = pdr.DataReader(company, 'yahoo', allDataStart, allDataEnd)
    calculateAndDraw(companyData, company)


getDataAndCalculate('AAPL')
getDataAndCalculate('AMZN')
getDataAndCalculate('GOOG')
getDataAndCalculate('GS')
getDataAndCalculate('IBM')
