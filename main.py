from pandas_datareader import data as pdr
import pandas as pd
import datetime
import math

# 選擇 2015 ~ 2018 年
allDataStart = datetime.datetime(2016, 10, 1)
allDataEnd = datetime.datetime(2018, 10, 1)

# 一個月的天數
dateRange = 30

# 計算波動率的次數
numberOfTimes = 500 - dateRange + 1

# VIX與公司的對照表
vixMap = {'AAPL': 'VXAPL',
          'AMZN': 'VXAZN',
          'GOOG': 'VXGOG',
          'GS': 'VXGS',
          'IBM': 'VXIBM'}


def drawChart(result, company):
    title = company + ' ( ' + str(dateRange) + ' days' + ' )'
    figure = result.plot(x='startDay', y='volatility', title=title)
    picture = figure.set_xlabel('Number of Times').get_figure()
    picture.savefig('.\\OUTPUT\\' + company + '\\' + company + '_' +
                    str(dateRange) + 'DAYS.png')


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


def readStockAndDraw(company):
    companyData = pdr.DataReader(company, 'yahoo', allDataStart, allDataEnd)
    companyData.sort_index(ascending=False, inplace=True)
    companyData.to_csv('.\\EXCEL\\' + company + '\\' + company + '.csv')
    data = companyData['Close']

    result = pd.DataFrame(columns=['startDay', 'endDay', 'volatility'])

    # 從第二個開始算，因為要看前一天去算差值
    print('\n---', company, '---')
    for start in range(1, numberOfTimes + 1):
        end = start + dateRange - 1
        populationMean = calculatePopulationMean(data, start, end)
        historicalVolatility = calculateVolatility(
            data, populationMean, start, end)

        print('startDay:', start, ', endDay:', end,
              ', volatility:', historicalVolatility)

        result = result.append({'startDay': start, 'endDay': end,
                                'volatility': historicalVolatility}, ignore_index=True)
    result.to_csv('.\\EXCEL\\' + company + '\\' + company + '_Result.csv')
    drawChart(result, company)


def readVIXAndDraw(company):
    vix = pd.read_csv('.\\VIX\\' + vixMap[company] + '.csv')
    vix['Date'] = pd.to_datetime(vix['Date'])
    result = vix[(vix['Date'] > allDataStart) & (vix['Date'] <= allDataEnd)]

    title = company + ' ( VIX )'
    figure = result.plot(x='Date', y='Close', title=title)
    picture = figure.set_xlabel('').get_figure()
    picture.savefig('.\\OUTPUT\\' + company + '\\' + company + '_VIX.png')


def getDataAndCalculate(company):
    readStockAndDraw(company)
    readVIXAndDraw(company)


getDataAndCalculate('AAPL')
getDataAndCalculate('AMZN')
getDataAndCalculate('GOOG')
getDataAndCalculate('GS')
getDataAndCalculate('IBM')
