
import config
from math import log
import statistics
import csv
def calcPVSlopes(r,symbol,conf):
    volume = []
    close = []
    endtime = []
    Mv =None
    Mp=None
    try:
        print(symbol)

        ohlc = r.zrevrange(symbol, 0, conf.tickWidth - 1)
        for i in ohlc:
            barData = r.hgetall(i)
            for key, value in barData.items():
                if str(key, 'utf-8') == "volume":
                    volume.append(int(value))
                elif str(key, 'utf-8') == "close":
                    close.append(float(value))
                elif str(key, 'utf-8') == "endtime":
                   endtime.append(int(value))

        #print('Volume: {}'.format(volume))
        #print('Close: {}'.format(close))
        #print('EndTime: {}'.format(endtime))

        # Volume calculations
        if len(close)>3:

            logVol = [log(x, conf.logBase) for x in volume]
            logVolMean = statistics.mean(logVol)
            #print('logVol: {} logVolMean: {}'.format(logVol, logVolMean))

            sumlogVol = []
            for i in range(len(logVol)):
                sumlogVol.append(logVol[i] - logVolMean)

            # Price calculations

            priceMean = statistics.mean(close)
            sumPrice = []
            for i in range(len(close)):
                sumPrice.append(close[i] - priceMean)

            # Time Calculations

            timeMean = statistics.mean(endtime)
            sumPrice = []
            for i in range(len(close)):
                sumPrice.append(close[i] - priceMean)

            timeI = []
            avgTime = []
            timeElements = len(endtime)
            basetime = endtime[timeElements - 1]
            for i in range(timeElements):
                x = (endtime[i] - basetime)
                timeI.append(x)
                avgTime.append((x / timeElements))
            timeMean = statistics.mean(timeI)
            sumtimeMean = sum(avgTime)
            finalTimeList = []
            for i in range(len(timeI)):
                finalTimeList.append(timeI[i] - timeMean)

            #print(avgTime)
            #print(timeI)
            #print(finalTimeList)
            #print('TimeMean:{},sumtimeMean:{}'.format(timeMean, sumtimeMean))
            #print('timeI: {}'.format(timeI))
            #print('sumPrice:{}'.format(sumPrice))
            #print('sumlogVol: {}'.format(sumlogVol))
            #print('Means---  Price:{}, logVol:{}, Time:{}'.format(priceMean, logVolMean, timeMean))

            numVolList = [sumlogVol[i] * finalTimeList[i] for i in range(len(finalTimeList))]
            timeSquaredList = [finalTimeList[i] * finalTimeList[i] for i in range(len(finalTimeList))]
            Mv = sum(numVolList) / sum(timeSquaredList)

            numPriceList = [sumPrice[i] * finalTimeList[i] for i in range(len(finalTimeList))]
            Mp = sum(numPriceList) / sum(timeSquaredList)
            #print(numVolList)
            #print(timeSquaredList)
            #print('Mv:{} Mp:{}'.format(Mv, Mp))
    except AssertionError as error:
            #print(error)
            print('Error calculating slopes for :{}'.format(symbol))
    return Mv, Mp,volume,close

