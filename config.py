from markettimings import is_open



marketDelay=0
tickWidth=0
logBase=0
startTime=None
endTime=None
timeinterval=None
finalList=None

def readfile():
    global marketDelay, tickWidth, logBase,startTime,endTime,timeinterval
    global isOpen

    with open("config.properties") as file_in:
        lines = [line.rstrip() for line in file_in]
        for x in lines:
            abv = (x.split(",", 2))
            if abv[0] == "StartTime":
                startTime = abv[1]
            elif abv[0] == "EndTime":
                endTime = abv[1]
            elif abv[0] == "MarketDelay":
                marketDelay = int(abv[1])
            elif abv[0] == "TickWidth":
                tickWidth = int(abv[1])
            elif abv[0] == "LogBase":
                logBase = int(abv[1])
            elif abv[0] == "TimeInterval":
                timeinterval = int(abv[1])
            elif abv[0] == "FinalList":
                finalList = int(abv[1])

    #print('StartTime: {} EndTime: {} MarketDelay: {} TickWidth: {} LogBase:{}'.format(startTime, endTime, marketDelay,tickWidth, logBase))

class Config:
  def __init__(self):
    readfile()
    self.marketDelay = marketDelay
    self.tickWidth = tickWidth
    self.startTime=startTime
    self.endTime=endTime
    self.logBase=logBase
    self.timeinterval=timeinterval
    self.finalList=finalList




