import redis
from calcSlopes import calcPVSlopes
from markettimings import is_open
import operator
import config
import json
from concurrent.futures import ThreadPoolExecutor

redisurl = 'redis://h:p178447b35881e7b0c20eb34bd323348b8fc25dbb93281eb32856044f5e7fff2c@ec2-34-234-161-22.compute-1.amazonaws.com:24149'
r = redis.from_url(redisurl)
conf = config.Config()
priceRank = {}
volRank = {}
combinedRank = {}
fireList = {}

def runForEachSymbol(symbol):
    global priceRank
    global volRank
    global combinedRank
    global fireList
    global r
    mv, mp, vol, close = calcPVSlopes(r, symbol)
    compSym = {"mp": mp, "mv": mv, "price": close[0], "pdiff1": close[0] - close[1], "pdiff2": close[0] - close[2],
               "pdiff3": close[0] - close[2],
               "vol": vol[0], "vdiff1": vol[0] - vol[1], "vdiff2": vol[0] - vol[2], "vdiff3": vol[0] - vol[2],
               "vRank": 0, "pRank": 0, "cRank": 0}

    if mp > 0:
        priceRank[symbol] = mp
        volRank[symbol] = mv
        combinedRank[symbol] = mp * mv
        fireList[symbol] = compSym


def gensignal():
    global conf
    global r
    global priceRank
    global volRank
    global combinedRank
    global fireList
    app_json='Test'
    if   is_open():
        symbolList=[]
        symbols = "symbols"
        symbolList = r.smembers(symbols)
        print(symbolList)
        symList = list(symbolList)[:1000]
        #symList=['ORCL']
        print('Running gensignal')
        with ThreadPoolExecutor(max_workers=15) as executor:
            for sym in symList:
                symbol=str(sym, 'utf-8')
                #symbol=sym
                print(symbol)
                executor.map(runForEachSymbol, symbol)


        n= conf.finalList
        if n==None:
            n=12

        priceRank = dict(sorted(priceRank.items(), key=operator.itemgetter(1), reverse=True)[:n])
        volRank = dict(sorted(volRank.items(), key=operator.itemgetter(1), reverse=True)[:n])
        combinedRank=dict(sorted(combinedRank.items(), key=operator.itemgetter(1), reverse=True)[:n*2])
        #print(priceRank)
        #print(volRank)
        #print(combinedRank)
        key_list = list(fireList.keys())
        #print('print list')
        #print(key_list)
        #print(fireList)
        for key in key_list:
            rec = fireList[key]

            if key in priceRank:
                rec["pRank"] =list(priceRank).index(key)
            if key in volRank:
                rec["vRank"] = list(volRank).index(key)
            if key in combinedRank:
                rec["cRank"] = list(combinedRank).index(key)

        key1_list = list(fireList.keys())
        for key in key1_list:
                rec = fireList[key]
                if rec["pRank"]>0 or rec["vRank"] >0 or  rec["cRank"]>0 :
                   print("allz well")
                else :
                    if key in fireList.keys():
                        del fireList[key]
        app_json = json.dumps(fireList)


    # print('Volume:{} Price:{} Combined{}'.format(len(volList),len(priceList),len(combineList)))


    #print(app_json)
    #print(len(fireList))

    return app_json

# gensignal()