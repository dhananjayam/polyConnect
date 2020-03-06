from flask import Flask, request, render_template,json
from flask_csv import send_csv
import numpy as np
import requests

app = Flask(__name__)


@app.route('/')
def index():
  # resp = requests.get("https://api.polygon.io/v2/ticks/stocks/trades/AAPL/2018-02-02?limit=10&apiKey=yWq25Y3mVWiADXve5h3bjKEp_3q1Tho9rM4U_R")

   # print(resp.json())

   return render_template ('index.html', data=[])


@app.route('/process', methods=['GET', 'POST'])
def process():


   #print (request.form.get('securityType'))

   resp = requests.get("https://api.polygon.io/v2/ticks/stocks/trades/AAPL/2018-02-02?limit=10&apiKey=yWq25Y3mVWiADXve5h3bjKEp_3q1Tho9rM4U_R")


   #return render_template ('index.html', data=resp.json())

   arr = np.asarray(resp.json().get('results'))


   return send_csv(arr, "test.csv", ['p', 'i', 'z', 's', 'x', 'q', 't', 'y', 'c'])

if __name__ == '__main__': app.run(debug=True)