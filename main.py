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
    # 先畫除了 Volume 以外的 Column
    result.drop(columns=['Volume']).plot()


# def toCSV(company):
#     with open(company + '.csv', 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['Spam'] * 5 + ['Baked Beans'])


def getVIX(company):
    print('-----\nVIX Not Yet!')


def calculatePopulationMean(data, start):
    firstDay = data[start]
    lastDay = data[start + dateRange - 1]
    differenceValue = abs(lastDay - firstDay)
    mean = math.log(differenceValue / firstDay) / dateRange

    return mean


def totalSum(data, mean, start):
    sumNum = 0
    startDay = start
    endDay = start + dateRange - 1

    for day in range(startDay, endDay):
        difference = data[day] - data[day-1]
        deltaTSquare = (1 / 365) ** 0.5
        result = (difference / (data[day] * deltaTSquare)
                  - mean * deltaTSquare) ** 2
        sumNum += result

    return sumNum


def calculateVolatility(data, mean, start):
    historicalVolatility = (
        totalSum(data, mean, start) / (dateRange - 1)) ** 0.5

    return historicalVolatility


def calculate(companyData, company):
    companyData.sort_index(ascending=False, inplace=True)
    companyData.to_csv('.\\output\\' + company + '.csv')
    data = companyData['Close']

    result = pd.DataFrame(columns=['startDay', 'endDay', 'volatility'])
    for start in range(numberOfTimes):
        populationMean = calculatePopulationMean(data, start)
        historicalVolatility = calculateVolatility(data, populationMean, start)

        startDay = start + 1
        endDay = start + dateRange

        print('startDay:', startDay, ", endDay:", endDay)
        print('historicalVolatility:', historicalVolatility, '\n')

        result = result.append({'startDay': startDay, 'endDay': endDay,
                                'volatility': historicalVolatility}, ignore_index=True)
    result.to_csv('.\\output\\' + company + '_result.csv')


def getDataAndCalculate(company):
    companyData = pdr.DataReader(company, 'yahoo', allDataStart, allDataEnd)
    calculate(companyData, company)


getDataAndCalculate('AAPL')
print('FINISH')
