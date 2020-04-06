
from flask import Flask, request, render_template, json, send_from_directory
from flask_csv import send_csv
from generateSignal import gensignal
import requests
import datetime
from multiprocessing import Process, Queue

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
  # resp = requests.get("https://api.polygon.io/v2/ticks/stocks/trades/AAPL/2018-02-02?limit=10&apiKey=yWq25Y3mVWiADXve5h3bjKEp_3q1Tho9rM4U_R")

  # print(resp.json())


  return render_template ('index.html', data=[])

@app.route('/data')
def serve_page():

    dataList = gensignal()
    print('I am in html')
    # print(app_json)
    return dataList

@app.route('/index')
def samplefunction():
    return render_template('v1/index-V2.html')

@app.route('/fetchData')
def sendData(data):

    print("data >> " + data)

    return "OK"






if __name__ == '__main__':

    app.run(debug=True)