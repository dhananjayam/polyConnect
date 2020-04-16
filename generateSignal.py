import redis
from calcSlopes import calcPVSlopes
from markettimings import is_open
import operator
import config
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pytz import timezone
import datetime

redisurl = 'redis://h:p178447b35881e7b0c20eb34bd323348b8fc25dbb93281eb32856044f5e7fff2c@ec2-3-234-145-181.compute-1.amazonaws.com:27899'
r = redis.from_url(redisurl)
conf = config.Config()
priceRank = {}
volRank = {}
combinedRank = {}
fireList = {}
mktOpen = is_open()

def runForEachSymbol(symbol):
    global priceRank
    global volRank
    global combinedRank
    global fireList
    global r
    global mktOpen
    symbol=str(symbol, 'utf-8')
    mv, mp, vol, close,endtime = calcPVSlopes(r, symbol,conf,mktOpen)
    if mp is not None:
        d = datetime.datetime.fromtimestamp(int(endtime[0]))
        ny = d.astimezone(timezone('US/Eastern'))

        #d1 = datetime.datetime.fromtimestamp(int(endtime[2]))
        dt =ny.isoformat()
        #dt1 =d.isoformat()
        #print('Symbol:{}, D0:{}, D1:{}'.format(symbol,d,d1))
        compSym = {"time": dt,"vRank": -1, "pRank": -1, "cRank": -1,"mp": mp, "mv": mv, "price": close[0], "pdiff1": close[0] - close[1], "pdiff2": close[0] - close[2],
                   "pdiff3": close[0] - close[2],
                   "vol": vol[0], "vdiff1": vol[0] - vol[1], "vdiff2": vol[0] - vol[2], "vdiff3": vol[0] - vol[2]
                   }
        #print(compSym)

        priceRank[symbol] = mp
        volRank[symbol] = mv
        combinedRank[symbol] = mp * mv
        fireList[symbol] = compSym


def gensignal():
    global conf
    app_json='Test'
    global priceRank
    global volRank
    global combinedRank
    global fireList
    global r
    global mktOpen
    dataList = {}
    startime =time.time()
    print('MktOpen:',mktOpen)



    symbolList=[]
    symbols = "symbols"
    symbolList = r.smembers(symbols)
    #print(symbolList)
    symCount =len(symbolList)
    print('symbolList:{}'.format(symCount))
    symList = list(symbolList) [:5000]
    #symList=['ORCL']
    print('Running gensignal')
    with ThreadPoolExecutor(max_workers=50) as executor:
        # for sym in symList:
        # symbol=str(sym, 'utf-8')
        # symbol=sym
        # print(symbol)
        for sym in executor.map(runForEachSymbol, symList):
            pass

    n= conf.finalList
    if n==None:
        n=12

    priceRank = dict(sorted(priceRank.items(), key=operator.itemgetter(1), reverse=True))
    volRank = dict(sorted(volRank.items(), key=operator.itemgetter(1), reverse=True))
    combinedRank=dict(sorted(combinedRank.items(), key=operator.itemgetter(1), reverse=True))
    #print(priceRank)
    #print(volRank)
    #print(combinedRank)
    key_list = list(fireList.keys())
    print('print list')
    print(len(fireList))
    #print(key_list)
    #print(fireList)
    for key in key_list:
        rec = fireList[key]

        mx = rec["mp"]

        #print(mx)
        if mx < 0.0:
            del fireList[key]
            continue

        if key in priceRank:
            rank =list(priceRank).index(key)
            rec["pRank"]=rank
            fireList.update(key=rec)
            #print(key,(list(priceRank).index(key)))
        if key in volRank:
            rec["vRank"] = list(volRank).index(key)
            #print(key, (list(volRank).index(key)))
            fireList.update(key=rec)
        if key in combinedRank:
            rec["cRank"] = list(combinedRank).index(key)
            #print(key, (list(combinedRank).index(key)))
            fireList.update(key=rec)



    key1_list = list(fireList.keys())
    for key in key1_list:
            rec = fireList[key]
            if ((rec["pRank"]>=0 and rec["pRank"]<12) or (rec["vRank"] >0 and rec["vRank"] <12) or  (rec["cRank"]>0 and rec["cRank"]<24)) :
               print("allz well")
            else :
                if key in fireList.keys():
                    del fireList[key]
    app_json = json.dumps(fireList)


    # print('Volume:{} Price:{} Combined{}'.format(len(volList),len(priceList),len(combineList)))


    #print(app_json)
    #print(len(fireList))

    endtime=time.time()

    print(app_json)
    print('Time taken to finish run:{}'.format(int(endtime - startime)))
    return app_json

#gensignal()