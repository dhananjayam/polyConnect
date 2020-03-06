from flask import Flask, request, render_template,json
from flask_csv import send_csv
import numpy as np
import requests
import datetime

app = Flask(__name__)


@app.route('/')
def index():
  # resp = requests.get("https://api.polygon.io/v2/ticks/stocks/trades/AAPL/2018-02-02?limit=10&apiKey=yWq25Y3mVWiADXve5h3bjKEp_3q1Tho9rM4U_R")

   # print(resp.json())

   return render_template ('index.html', data=[])


@app.route('/process', methods=['GET', 'POST'])
def process():


   secType = (request.form.get('securityType'))
   symbol =  (request.form.get('symbol'))
   timeframe = (request.form.get('timeframe'))
   fromDt = (request.form.get('fromDt'))
   toDt = (request.form.get('toDt'))


   symbol=symbol.upper()
   timeframe=timeframe.lower()
   print(symbol)
   print(timeframe)

   if secType == "Currency" :
       symbol ="C:"+symbol
   elif secType == "Crypto" :
       symbol="X:"+symbol

   frmtime = datetime.datetime.strptime(fromDt, '%m/%d/%Y')
   dt = frmtime.date()
   fromStr=dt.strftime("%Y-%m-%d")

   totime = datetime.datetime.strptime(toDt, '%m/%d/%Y')
   todt = totime.date()
   toStr = todt.strftime("%Y-%m-%d")
   mutiplier="1"

   if timeframe =="5 Min":
       mutiplier="5"
       timeframe="minute"
   elif timeframe =="30 Min":
       mutiplier="30"
       timeframe="minute"

   print(fromStr)

   urlStr="https://api.polygon.io/v2/aggs/ticker/"+symbol+"/range/"+mutiplier+"/"+timeframe+"/"+fromStr+"/"+toStr+"?unadjusted=true&apiKey=yWq25Y3mVWiADXve5h3bjKEp_3q1Tho9rM4U_R"


   resp = requests.get(urlStr)

   #return render_template ('index.html', data=resp.json())

   arr = np.asarray(resp.json().get('results'))


   return send_csv(arr, "test.csv", ['v', 'vw', 'o', 'c', 'h', 'l', 't', 'n'])



if __name__ == '__main__': app.run(debug=True)