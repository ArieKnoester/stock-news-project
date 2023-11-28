import requests
from twilio.rest import Client
# from test_data import test_stock_data, test_news_data  # Testing

# For security, all sensitive constants (keys, id's, tokens, phone #s) should be implemented
# as environment variables. However, I will not be running this code on a live server. This
# is just a one-off project for learning purposes.
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
TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""
TWILIO_PHONE_NUMBER = ""
RECIPIENT_PHONE_NUMBER = ""


def request_stock_data():
    # return test_stock_data  # Testing
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
    return round(percent_delta, 1)


def request_recent_news():
    response = requests.get(NEWSAPI_ENDPOINT, NEWSAPI_PARAMETERS)
    response.raise_for_status()
    return response.json()["articles"]


def sms_recent_news_articles(articles, percent_change):
    if percent_change < 0:
        icon = "🔻"
    else:
        icon = "🔺"
    for article in articles:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"""
                \n{STOCK}: {icon}{percent_change}%
                Headline: {article["title"]}.
                Brief: {article["description"]}.
                Link: {article["url"]}
                """,
            from_=TWILIO_PHONE_NUMBER,
            to=RECIPIENT_PHONE_NUMBER
        )
        print(message.status)


# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
delta = calculate_closing_price_percentage_delta()
print(f"delta: {delta}")

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
# if True:  # Testing
if delta <= -5.0 or delta >= 5.0:
    # print("Get news.")
    # news_articles = test_news_data["articles"]  # Testing
    news_articles = request_recent_news()
    # print(news_articles)

    # STEP 3: Use https://www.twilio.com
    # Send a separate message with the percentage change and each article's title and description to your phone number.
    sms_recent_news_articles(articles=news_articles, percent_change=delta)
else:
    # Sanity check.
    print("Less than 5% difference in closing values.")
