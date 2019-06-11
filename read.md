Simple Application that scrapes prices of gold and silve off the following websites:

https://www.investing.com/commodities/gold-historical-data
https://www.investing.com/commodities/silver-historical-data

It then creates end points to a http get request in a specified format:

e.g
http://127.0.0.1:8080/commodity?start_date=2019-05-10&end_date=2019-06-22&commodity_type=gold

Returns a json in the following format
{
data: {
2019-05-13: 1301.8,
2019-05-14: 1296.3,
2019-05-15: 1297.8,
2019-05-16: 1286.2,
2019-05-17: 1275.7,
2019-05-20: 1277.3,
2019-05-21: 1273.2,
2019-05-22: 1274.2,
2019-05-23: 1285.4,
2019-05-24: 1283.6,
2019-05-26: 1284.15,
2019-05-27: 1284.95,
2019-05-28: 1277.1,
2019-05-29: 1281,
2019-05-30: 1287.1,
2019-05-31: 1305.8,
2019-06-03: 1322.7,
2019-06-04: 1323.4,
2019-06-05: 1328.3,
2019-06-06: 1337.6,
2019-06-07: 1341.2,
2019-06-10: 1324.7,
2019-06-11: 1330.55
},
mean: 1299.134347826087,
variance: 493.4666826849733
}

How to run application:
Make sure you have the following modules installed as they are being used in the app

Modules: flask,request,bs4,pymongo
..
tell the terminal the application to run with:
export FLASK_APP = app.py 

run the app,setting the port number to 8080. Default is 5000
flask run --port=8080
