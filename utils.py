import requests
import bs4
import json
import statistics
from datetime import datetime


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

def queryCommodity(cType,startTime,endTime,client):
    # Showcasing the count() method of find, count the total number of 5 ratings 
    date1 = datetime.strptime(startTime,'%Y-%m-%d')
    date2 = datetime.strptime(endTime,'%Y-%m-%d')

    # yearMonthDayUTC: { $dateToString: { format: "%Y-%m-%d", date: "$date" } }
    pipeline = [{'$match':{'date':{'$gte':date1,'$lte':date2},'type':cType}},
    {'$sort' :{'date':1}},
    {'$project' : {"date":{'$dateToString':{'format':'%Y-%m-%d','date':'$date'}},
    "price":1,'_id':0}
    }]
    #add $lt range later
    goldCommodities = client.commodities.aggregate(pipeline)
    prices = []
    data = {}
    result = {}
    for commodity in goldCommodities:
        data[commodity.get('date')] = commodity.get('price')
        prices.append(commodity.get('price'))

    # print(prices)
    if(len(prices) == 0):
        # There was no match
        return json.dumps({'Error':'There was no matching commodity'})
    cMean = statistics.mean(prices)
    cVariance=statistics.variance(prices)

    result['data'] = data
    result['mean'] = cMean
    result['variance'] = cVariance

    return json.dumps(result)
    # pprint.pprint(commodity.get('price'))
    