import requests
# from test_data import stock_data, news_data

STOCK = "NVDA"
COMPANY_NAME = "Nvidia"
# Below comment is for Pycharm,
# so that it doesn't flag the api key as a misspelled word.
# noinspection SpellCheckingInspection
ALPHAVANTAGE_API_KEY = ""
# API is limited to 25 free requests per day.
# Use the stock_data dict in test_data.py for testing.
ALPHAVANTAGE_ENDPOINT = "https://www.alphavantage.co/query"
ALPHAVANTAGE_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": ALPHAVANTAGE_API_KEY
}
NEWSAPI_API_KEY = ""
# API limited to 1000 free requests within 24 hours.
NEWSAPI_ENDPOINT = "https://newsapi.org/v2/everything"
NEWSAPI_PARAMETERS = {
    "apiKey": NEWSAPI_API_KEY,
    "q": COMPANY_NAME,
    "language": "en",
    "pageSize": 3,
    "sortBy": "relevancy,popularity,publishedAt"
}


def request_stock_data():
    response = requests.get(ALPHAVANTAGE_ENDPOINT, ALPHAVANTAGE_PARAMETERS)
    response.raise_for_status()
    return response.json()["Time Series (Daily)"]


def calculate_closing_price_percentage_delta():
    stock_data = request_stock_data()
    closing_prices_past_two_days = [float(date["4. close"]) for date in list(stock_data.values())[:2]]
    # print(closing_prices_past_two_days)
    current_closing_price = closing_prices_past_two_days[0]
    previous_closing_price = closing_prices_past_two_days[1]
    percent_delta = ((current_closing_price - previous_closing_price) / previous_closing_price) * 100
    return percent_delta


def request_recent_news():
    response = requests.get(NEWSAPI_ENDPOINT, NEWSAPI_PARAMETERS)
    response.raise_for_status()
    return response.json()


# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
delta = calculate_closing_price_percentage_delta()
# print(f"delta: {delta}")

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
# if True:  # Testing
if delta < -5 or delta > 5:
    # print("Get news.")
    news_data = request_recent_news()
    # print(news_data)

    # STEP 3: Use https://www.twilio.com
    # Send a separate message with the percentage change and each article's title and description to your phone number.
else:
    # Sanity check.
    print("Less than 5% difference in closing values.")

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
