
import config
from math import log
import statistics
import csv
import time
from concurrent.futures import ThreadPoolExecutor
red=None

def getBarData(i):
		barData = red.hgetall(i)
		return barData


def calcPVSlopes(r,symbol,conf,mktOpen):
    global red
    volume = []
    close = []
    endtime = []
    barData=[]
    Mv =None
    Mp=None
    red= r
    try:
        print(symbol)

        ohlc = r.zrevrange(symbol, 0, conf.tickWidth - 1)
        #print ('lEN.OHLG:{} OHLC:{}'.format(len(ohlc),ohlc))
        if len(ohlc)== conf.tickWidth:
           # with ThreadPoolExecutor(max_workers=2) as executor:
           #     results = executor.map(getBarData, ohlc)
           #     for barData in results:
                    #print('barDate:{}'.format(barData))
            x=0
            for i in ohlc:
                    barData = r.hgetall(i)
                    x=x+1
                    for key, value in barData.items():
                        if str(key, 'utf-8') == "volume":
                            volume.append(int(value))
                        elif str(key, 'utf-8') == "close":
                            close.append(float(value))
                        elif str(key, 'utf-8') == "endtime":
                            endtime.append(int(value))
                            millis = int(round(time.time()))
                            #print('i =',i)
                            if x==1 and mktOpen :
                                #print('Symbol: {}, CurrentTime: {} LatestBar:{}'.format(symbol, str(millis), str(value)))
                                if int(value) < (millis - 120):
                                    return Mv, Mp,volume,close,endtime




                #print('Volume: {}'.format(volume))
                #print('Close: {}'.format(close))
                #print('EndTime1: {}'.format(endtime))

            # Volume calculations
            if len(endtime)>3:

                logVol = [log(x, conf.logBase) for x in volume]
                logVolMean = statistics.mean(logVol)
                #print('logVol: {} logVolMean: {}'.format(logVol, logVolMean))

                sumlogVol = []
                for i in range(len(logVol)):
                    sumlogVol.append(logVol[i] - logVolMean)

                # Price calculations

                #print('Closes:{}'.format(len(close)))
                basePrice = close[len(close)-1]
                #print(close)
                #print (basePrice)
                pctPriceChg = []
                for i in range(len(close)):
                    pctPriceChg.append((close[i] - basePrice)*100/basePrice)

                pctPriceChgMean=  statistics.mean(pctPriceChg)

                sumPrice = []
                for i in range(len(pctPriceChg)):
                    sumPrice.append(pctPriceChg[i] - pctPriceChgMean)

                # Time Calculations

                timeMean = statistics.mean(endtime)

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
                #print('Means---  Price:{}, logVol:{}, Time:{}'.format(pctPriceChgMean, logVolMean, timeMean))
                #print(pctPriceChg)

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
    return Mv, Mp,volume,close,endtime

