import time
from datetime import datetime, time
import config
import calendar


marketDelay=0
tickWidth=0
logBase=0


def is_weekend():
    weekday = datetime.datetime.today().weekday() # weekday as a number
    if weekday in [calendar.SATURDAY, calendar.SUNDAY]:
        return True

    return False


def is_open():
    global marketDelay,tickWidth,logBase
    conf = config.Config()
    StartTime = config.startTime
    EndTime=config.endTime
    marketDelay=config.marketDelay


    print('StartTime: {} EndTime: {} MarketDelay: {}  CurrentTime: {}'.format(StartTime, EndTime, marketDelay,datetime.now().time()))

    curTime = datetime.now().time()
    startHour = int(StartTime.split(":", 2)[0])
    startMinute = int(StartTime.split(":", 2)[1])
    endHour = int(EndTime.split(":", 2)[0])
    endMinute = int(EndTime.split(":", 2)[1])
    startMinute=startMinute+marketDelay
    if startMinute>60:
        hrs = startMinute//60
        startMinute=startMinute-(hrs*60)
        startHour=startHour+hrs
        print('startTime:{}:{}'.format(startHour,startMinute))

    if curTime >= time(startHour, startMinute) and curTime <= time(endHour, endMinute):
        print('I am in working hours')
    else:
        return False
    print('Hour:{} Minute:{}'.format(startHour, startMinute))

    if is_weekend:
              # TEMP
        weekno = datetime.today().weekday()
        print(weekno)
        if weekno >= 5:
            print(f': today is weekend')
            return False
        else:
            return True



if __name__ == '__main__':
    print(f'market_timing.py. Test is_exchange_open()\n')
    if is_open():
        print("We are working")
    else:
        print('Market is closed')