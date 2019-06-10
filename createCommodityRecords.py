import requests
import bs4
from pymongo import MongoClient
from datetime import datetime

goldURL = 'https://www.investing.com/commodities/gold-historical-data'
silevrURL = 'https://www.investing.com/commodities/silver-historical-data'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


def extractDateAndPrices(url,client,commodityType):
    res = requests.get(url,headers = headers)
    soup = bs4.BeautifulSoup(res.text,'lxml')

    for row in soup.find('table',id="curr_table").tbody.find_all('tr'):
        columns = row.find_all('td')
        date = datetime.strptime(columns[0].get_text(),'%b %d, %Y')
        price = float(columns[1].get_text().replace(',',''))

        commodity = {
            'date':date,
            'price':price,
            'type':commodityType
        }
        #Step 3: Insert business object directly into MongoDB via isnert_one
        result = client.commodities.insert_one(commodity)
        
        #Step 4: Print to the console the ObjectID of the new document
        print('Created {0} with id of {1}'.format(commodity,result.inserted_id))

#Step 1: Connect to MongoDB
client = MongoClient('mongodb://127.0.0.1:27017')
db=client.trading

#extract gold prices and silver prices
extractDateAndPrices(goldURL,db,'gold')
extractDateAndPrices(silevrURL,db,'silver')