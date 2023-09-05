from flask import Flask, render_template
import requests
import json
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/api/calculate', methods=['GET', 'POST'])
def calculate(event, context):



   
    # Assuming the data was sent as a JSON object in the request body
    # Parse the JSON data from the event's 'body' field
    data = json.loads(event['body'])
    # Now 'data' will be a dictionary containing the keys "Stock Symbol", "Amount Invested", and "Date Invested"

    # Access the values from the 'data' dictionary
    symbol = data.get('Stock Symbol')
    amount_invested = data.get('Amount Invested')
    date_invested = data.get('Date Invested')


    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + symbol + '&outputsize=full&apikey=TSH9AYE3COXT80GI'
    response = requests.get(url)
    data = response.json()

    time_series_daily = data["Time Series (Daily)"]
    most_recent_date = max(datetime.strptime(date, '%Y-%m-%d').date() for date in time_series_daily.keys())
    most_recent_date_str = most_recent_date.strftime('%Y-%m-%d')

   
    starting_stock_price = float(data["Time Series (Daily)"][date_invested]["5. adjusted close"])
    current_stock_price = float(data["Time Series (Daily)"][most_recent_date_str]["5. adjusted close"])

    shares_owned_initially = amount_invested // starting_stock_price

    print()
    print("Starting stock price was " + str(round(starting_stock_price, 2)))
    print("Number of shares you initially own" + str(round(shares_owned_initially, 2)))



    # Extract the Time Series (Daily) data
    

    

    # Loop through the data and find the times when dividend amount is not equal to 0
    dividend_not_zero_dates = []
    total_shares_owned = shares_owned_initially
    for date, values in time_series_daily.items():
        dividend_amount = float(values["7. dividend amount"])
        

        if dividend_amount != 0:
            current_price = float(values["5. adjusted close"])
            new_shares_bought = dividend_amount / current_price
            total_shares_owned += new_shares_bought
            dividend_not_zero_dates.append(date)

    # print("Dates when dividend amount is not equal to 0:")
    # print(dividend_not_zero_dates)
    print("number of shares you now own "+ str(round(total_shares_owned, 2)))
    current_value = total_shares_owned * current_stock_price
    print("Your money would be worth " + str(round(current_value, 2)))











def calculate2(event, context):

    inp = input("Enter symbol: ")
    amount_invested = int(input("How much to invest? "))
    date_invested = input("When to invest (yyyy-mm-dd)?")

    inp2 = event['Stock Symbol']
    inp


    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + inp + '&outputsize=full&apikey=TSH9AYE3COXT80GI'
    response = requests.get(url)
    data = response.json()

    time_series_daily = data["Time Series (Daily)"]
    most_recent_date = max(datetime.strptime(date, '%Y-%m-%d').date() for date in time_series_daily.keys())
    most_recent_date_str = most_recent_date.strftime('%Y-%m-%d')

   
    starting_stock_price = float(data["Time Series (Daily)"][date_invested]["5. adjusted close"])
    current_stock_price = float(data["Time Series (Daily)"][most_recent_date_str]["5. adjusted close"])

    shares_owned_initially = amount_invested // starting_stock_price

    print()
    print("Starting stock price was " + str(round(starting_stock_price, 2)))
    print("Number of shares you initially own" + str(round(shares_owned_initially, 2)))



    # Extract the Time Series (Daily) data
    

    

    # Loop through the data and find the times when dividend amount is not equal to 0
    dividend_not_zero_dates = []
    total_shares_owned = shares_owned_initially
    for date, values in time_series_daily.items():
        dividend_amount = float(values["7. dividend amount"])
        

        if dividend_amount != 0:
            current_price = float(values["5. adjusted close"])
            new_shares_bought = dividend_amount / current_price
            total_shares_owned += new_shares_bought
            dividend_not_zero_dates.append(date)

    # print("Dates when dividend amount is not equal to 0:")
    # print(dividend_not_zero_dates)
    print("number of shares you now own "+ str(round(total_shares_owned, 2)))
    current_value = total_shares_owned * current_stock_price
    print("Your money would be worth " + str(round(current_value, 2)))




    

    # if response.status_code == 200:
    #     # Parse JSON response
    #     selected_data = [[candle[0], candle[4]] for candle in btc_candle_data]
    #     sorted_data = sorted(selected_data, key=lambda x: x[0])

    #     return {
    #         "statusCode": 200,
    #         "body": sorted_data
    #         #"body": json.dumps(selected_data)
    #     }
    # else:
    #     return {
    #         "statusCode": response.status_code,
    #         "body": response.text
    #     }




if __name__ == '__main__':
    app.run()
  

