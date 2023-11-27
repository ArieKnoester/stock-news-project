import requests
from stock_data import stock_data  # For testing

STOCK = ""
COMPANY_NAME = ""
ALPHAVANTAGE_API_KEY = ""
# Endpoint is limited to 25 free requests per day.
# Use the dict in stock_data.py for testing.
ALPHAVANTAGE_ENDPOINT = "https://www.alphavantage.co/query"
ALPHAVANTAGE_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": ALPHAVANTAGE_API_KEY
}
# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# response = requests.get(ALPHAVANTAGE_ENDPOINT, ALPHAVANTAGE_PARAMETERS)
# response.raise_for_status()
# stock_data = response.json()["Time Series (Daily)"]
print(stock_data)
closing_prices_past_two_days = [float(date["4. close"]) for date in list(stock_data.values())[:2]]
print(closing_prices_past_two_days)
closing_price_previous_day = closing_prices_past_two_days[0]
closing_price_day_before_previous_day = closing_prices_past_two_days[1]
percent_difference = (
    (closing_price_previous_day - closing_price_day_before_previous_day) / closing_price_day_before_previous_day * 100
)
if percent_difference < -5 or percent_difference > 5:
    print("Get news.")
else:
    print("Less than 5% difference in closing values.")
# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

# STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


# Optional: Format the SMS message like this:
# """
# TSLA: 🔺2%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to
# file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height
# of the coronavirus market crash.
# or
# "TSLA: 🔻5%
# Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?.
# Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to
# file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height
# of the coronavirus market crash.
# """
