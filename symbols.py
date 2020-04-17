
import datetime
import requests
import csv

def getSymbols():
    symfile =open("symbols.csv","r")
    lines=symfile.readlines()
    symList=[]
    x=0
    for line in lines:
        if x==0:
            inputDt =line
            today = datetime.date.today()
            d1 = today.strftime("%Y-%m-%d")
            if d1==inputDt:
                symList=1
        else:
            symList=line.split (",")
        x=x+1
    return symList

def getYestPrice():
    today = datetime.date.today()
    offset = max(1, (today.weekday() + 6) % 7 - 3)
    timedelta = datetime.timedelta(offset)
    most_recent = today - timedelta
    d1 = most_recent.strftime("%Y-%m-%d")
    print(d1)
    urlStr = "https://api.polygon.io/v2/aggs/grouped/locale/US/market/STOCKS/"+d1+"?apiKey=yWq25Y3mVWiADXve5h3bjKEp_3q1Tho9rM4U_R"
    print(urlStr)
    symList =[]
    resp = requests.get(urlStr)
    ray = (resp.json().get('results'))
    print(ray)
    for rec in ray:
       close = rec.pop("c")
       vol = rec.pop("v")
       sym =rec.pop("T")
       if close>1 and vol >100000:
            symList.append(sym)
            print(sym)


    if len(symList)>1:
        with open('symbols.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([d1])
            writer.writerow(symList)