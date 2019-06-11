import utils
import time
from flask import Flask
from flask import request
from pymongo import MongoClient

goldURL = 'https://www.investing.com/commodities/gold-historical-data'
silevrURL = 'https://www.investing.com/commodities/silver-historical-data'


#Step 1: Connect to MongoDB
retry_count = 0
try:
    client = MongoClient()
except Exception as exc:
    if retry_count > 20:
        raise Exception("Retries exceeded") from exc
    retry_count += 1
    time.sleep(6)
db=client.trading

#extract prices and insert into data base
utils.extractDateAndPrices(goldURL,db,'gold')
utils.extractDateAndPrices(silevrURL,db,'silver')

app = Flask(__name__)

@app.route('/')
def index():
    return "Index Page"
@app.route('/commodity')
def commodity():
    res = utils.queryCommodity(request.args.get('commodity_type'),request.args.get('start_date'),request.args.get('end_date'),db)
    return res


