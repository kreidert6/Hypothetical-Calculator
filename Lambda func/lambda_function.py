import requests
import json
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP

def lambda_handler(event, context):


    # Assuming the data was sent as a JSON object in the request body
    # Parse the JSON data from the event's 'body' field
    user_data = json.loads(event['body'])
    # Now 'data' will be a dictionary containing the keys "Stock Symbol", "Amount Invested", and "Date Invested"

    # Access the values from the 'data' dictionary
    symbol = user_data.get('Stock Symbol')
    amount_invested = user_data.get('Amount Invested')
    date_invested = user_data.get('Date Invested')
    
    apiKey2 = 'SPSP0HM95OEYQUXV'
    apiKey1 = 'TSH9AYE3COXT80GI'
    
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=' + symbol + '&outputsize=full&apikey=TSH9AYE3COXT80GI'
    response = requests.get(url)
    data = response.json()
    
    
    time_series_daily = data["Time Series (Daily)"]

    while date_invested not in time_series_daily:
        # Move the date one day back until a valid trading day is found
        date_invested = (datetime.strptime(date_invested, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")

    
    most_recent_date = max(datetime.strptime(date, '%Y-%m-%d').date() for date in time_series_daily)
    most_recent_date_str = most_recent_date.strftime('%Y-%m-%d')

   
    starting_stock_price = float(data["Time Series (Daily)"][date_invested]["5. adjusted close"])
    current_stock_price = float(data["Time Series (Daily)"][most_recent_date_str]["5. adjusted close"])

    shares_owned_initially = int(amount_invested) // starting_stock_price


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

    
    current_value = total_shares_owned * current_stock_price
    current_value = round(current_value, 2)
   
     
    return {
        'statusCode': 200,                # Desired status code
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'current_value': current_value
        }),    # Convert your data to JSON string
    }


