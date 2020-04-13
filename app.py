
from flask import Flask, request, render_template, json, send_from_directory
from flask_csv import send_csv
from generateSignal import gensignal
import requests
import datetime
from multiprocessing import Process, Queue
import fileinput
import configparser

app = Flask(__name__, static_folder="static")

@app.route('/')
def index():
  # resp = requests.get("https://api.polygon.io/v2/ticks/stocks/trades/AAPL/2018-02-02?limit=10&apiKey=yWq25Y3mVWiADXve5h3bjKEp_3q1Tho9rM4U_R")

  # print(resp.json())


  return render_template ('index.html', data=[])

@app.route('/data')
def serve_page():

    dataList = gensignal()
    # print('I am in html')
    # print(app_json)
    return dataList

@app.route('/index')
def samplefunction():
    return render_template('v1/index-V2.html')

@app.route('/fetchData', methods = ['POST'])
def sendData():
    # jsonData = request.get_json()['headers'] # response.json()['headers']
    # request.form.get("xh", None)
    # print(request.form.get("xh", None))

    mktDelay = request.form.get("marketDelay", None)
    tickWidth = request.form.get("tickWidth", None)
    logBase = request.form.get("logBase", None)
    print (mktDelay)

    y="MarketDelay," + mktDelay
    print(y)

    x = fileinput.input(files="config.properties", inplace=1)
    for line in x:
        if mktDelay is not None and mktDelay.isdigit and "MarketDelay" in line:
            abc = "MarketDelay," + mktDelay
            print('{}'.format(abc))
        elif tickWidth is not None and tickWidth.isdigit and "TickWidth" in line:
            abc = "TickWidth," + tickWidth
            print('{}'.format(abc))
        elif logBase is not None and logBase.isdigit() and "LogBase" in line:
            abc = "LogBase," + logBase
            print('{}'.format(abc))
        else:
            print('{}'.format(line),end='')
    x.close()
    """
    text = open("config.properties").read()
    if mktDelay is not None and mktDelay.isdigit:
        new_text = '\n'.join(y if "MarkeyDelay" in line else line
                             for line in text.splitlines())
    open("config.properties", 'w').write(new_text)

    """

    return "OK"

@app.route('/getMtlConfigData')
def mtlConfigData():
    global mktDelay
    global tickWidth
    global logBase
    x = fileinput.input(files="config.properties")
    for line in x:
        if "MarketDelay" in line:
            mktDelay = line.split(',', 1)[1]

        if "TickWidth" in line:
            tickWidth = line.split(',', 1)[1]

        if "LogBase" in line:
            logBase = line.split(',', 1)[1]

    x.close()

    # print(mktDelay)
    # print(tickWidth)
    # print(logBase)

    mtlData = {
        "marketDelay" : mktDelay.strip(),
        "tickWidth" : tickWidth.strip(),
        "logBase" : logBase.strip()
    }

    return mtlData


if __name__ == '__main__':

    app.run(debug=True)