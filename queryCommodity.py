from pymongo import MongoClient
from datetime import datetime
import pprint
import statistics
# Connect to the MongoDB, change the connection string per your MongoDB environment
client = MongoClient()
# Set the db object to point to the trading
db=client.trading

# Showcasing the count() method of find, count the total number of 5 ratings 
date1 = datetime.strptime('2019-06-06','%Y-%m-%d')
date2 = datetime.strptime('2019-06-10','%Y-%m-%d')

# yearMonthDayUTC: { $dateToString: { format: "%Y-%m-%d", date: "$date" } }
pipeline = [{'$match':{'date':{'$gte':date1,'$lte':date2},'type':'gold'}},
{'$sort' :{'date':1}},
{'$project' : {"date":{'$dateToString':{'format':'%Y-%m-%d','date':'$date'}},
"price":1,'_id':0}
}]
#add $lt range later
goldCommodities = db.commodities.aggregate(pipeline)
prices = []
for commodity in goldCommodities:
    pprint.pprint(commodity)
    prices.append(commodity.get('price'))

print('mean =',statistics.mean(prices))
print('variance = ',statistics.variance(prices))
# pprint.pprint(commodity.get('price'))