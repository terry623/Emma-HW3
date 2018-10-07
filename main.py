from pandas_datareader import data as pdr
import pandas as pd
import datetime
import math

# 選擇 2015 ~ 2018 年
allDataStart = datetime.datetime(2016, 10, 1)
allDataEnd = datetime.datetime(2018, 10, 1)

# 計算的天數範圍
dateRange = 30

# 計算波動率的次數
numberOfTimes = 500 - dateRange + 1

# VIX與公司的對照表
vixMap = {'AAPL': 'VXAPL',
          'AMZN': 'VXAZN',
          'GOOG': 'VXGOG',
          'GS': 'VXGS',
          'IBM': 'VXIBM'}


# 將波動率結果畫出來，並輸出成圖片
def drawChart(result, company):
    title = company + ' ( ' + str(dateRange) + ' days' + ' )'
    resultPlot = result.plot(x='startDay', y='volatility', title=title)
    figure = resultPlot.set_xlabel('Number of Times').get_figure()
    figure.savefig('.\\OUTPUT\\' + company + '\\' + company + '_' +
                    str(dateRange) + 'DAYS.png')


# 依照公式計算母體平均，並回傳結果
def calculatePopulationMean(data, start, end):
    firstDay = data[start]
    lastDay = data[end]
    differenceValue = abs(lastDay - firstDay)
    mean = math.log(differenceValue / firstDay) / dateRange

    return mean


# 計算波動率時，關於總合的部分
def totalSum(data, mean, start, end):
    sumNum = 0

    for day in range(start, end):
        difference = data[day] - data[day-1]
        deltaTSquare = (1 / 365) ** 0.5
        result = (difference / (data[day] * deltaTSquare)
                  - mean * deltaTSquare) ** 2
        sumNum += result

    return sumNum


# 依照公式計算波動率，並回傳結果
def calculateVolatility(data, mean, start, end):
    historicalVolatility = (
        totalSum(data, mean, start, end) / (dateRange - 1)) ** 0.5

    return historicalVolatility


def readStockAndDraw(company):
    # 從 pandas_datareader 獲取資料並排序
    companyData = pdr.DataReader(company, 'yahoo', allDataStart, allDataEnd)
    companyData.sort_index(ascending=False, inplace=True)

    # 將拿到的原始資料輸出成 CSV 檔，方便自己觀看
    companyData.to_csv('.\\EXCEL\\' + company + '\\' + company + '.csv')

    # 只選取收盤價
    data = companyData['Close']

    # 創建一個空的 DataFrame
    result = pd.DataFrame(columns=['startDay', 'endDay', 'volatility'])

    print('\n---', company, '---')
    for start in range(1, numberOfTimes + 1):
        end = start + dateRange - 1

        # 計算母體平均
        populationMean = calculatePopulationMean(data, start, end)

        # 計算波動率
        historicalVolatility = calculateVolatility(
            data, populationMean, start, end)

        # 將結果印出來，方便自己觀看
        print('startDay:', start, ', endDay:', end,
              ', volatility:', historicalVolatility)

        # 將每次計算後結果，新增到一開始創建的空 DataFrame
        result = result.append({'startDay': start, 'endDay': end,
                                'volatility': historicalVolatility}, ignore_index=True)

    # 將最後的 DataFrame 輸出成 CSV 檔，方便自己觀看
    result.to_csv('.\\EXCEL\\' + company + '\\' + company + '_Result.csv')

    # 把結果畫出來
    drawChart(result, company)


def readVIXAndDraw(company):
    # 讀取已經下載好的VIX資料
    vix = pd.read_csv('.\\VIX\\' + vixMap[company] + '.csv')

    # 並選取指定的時間範圍
    vix['Date'] = pd.to_datetime(vix['Date'])
    result = vix[(vix['Date'] > allDataStart) & (vix['Date'] <= allDataEnd)]

    # 將資料畫出來，並輸出成圖片
    title = company + ' ( VIX )'
    resultPlot = result.plot(x='Date', y='Close', title=title)
    figure = resultPlot.set_xlabel('').get_figure()
    figure.savefig('.\\OUTPUT\\' + company + '\\' + company + '_VIX.png')


# 作業要求的兩件工作
def getDataAndCalculate(company):
    # 從 Yahoo 讀資料並計算歷史波動率
    readStockAndDraw(company)

    # 讀取從 CBOE 下載的 VIX 資料
    readVIXAndDraw(company)


# 從這裡填入你要的公司代號
getDataAndCalculate('AAPL')
getDataAndCalculate('AMZN')
getDataAndCalculate('GOOG')
getDataAndCalculate('GS')
getDataAndCalculate('IBM')
