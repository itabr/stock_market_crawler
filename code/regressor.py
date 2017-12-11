import pandas as pd
import io
import requests
import time
import matplotlib.pyplot as plt

from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def google_stocks(symbol, shiftby=-1, startdate = (1, 1, 2006), enddate = None):

    startdate = str(startdate[0]) + '+' + str(startdate[1]) + '+' + str(startdate[2])

    if not enddate:
        enddate = time.strftime("%m+%d+%Y")
    else:
        enddate = str(enddate[0]) + '+' + str(enddate[1]) + '+' + str(enddate[2])

    stock_query = "http://finance.google.com/finance/historical?q=" + symbol + \
                "&startdate=" + startdate + "&enddate=" + enddate + "&output=csv"

    print (stock_query)

    raw_response = requests.get(stock_query).content

    stock_data = pd.read_csv(io.StringIO(raw_response.decode('utf-8')))
    stock_data['Date'] = stock_data['Date'].apply(lambda x: datetime.strptime(x, '%d-%b-%y').date())
    stock_data['Changes'] = stock_data['Close'] - stock_data['Close'].shift(shiftby)
    # stock_data['Date'] = stock_data['Date'].apply(lambda x: str(x))
    stock_data.to_csv('../data/stock_price.csv')
    return stock_data

def get_sentiment_data(csv):
    sentiment_data = pd.read_csv('../data/tweets_classifed_using_classifier.csv')
    sentiment_data.columns = ['Classification', 'Date', 'Tweet']
    sentiment_data = sentiment_data.drop('Tweet', axis=1)

    # Replace date string with date objects
    for index, row in sentiment_data.iterrows():
        datestring = row['Date'][4:10] + " " + row['Date'][-4:]
        datetime_object = datetime.strptime(datestring, '%b %d %Y')
        sentiment_data.at[index, 'Date'] = datetime_object.date()

    # Get classification counts per day
    sentiment_data_count = pd.DataFrame({'count' : sentiment_data.groupby( [ "Date", "Classification"] ).size()}).reset_index()
    sentiment_data_count = sentiment_data_count.pivot(index='Date', columns='Classification', values='count').reset_index()
    sentiment_data_count.to_csv('../data/sentiment_data.csv')
    return sentiment_data_count

def get_final_data(sentiment_data, stock_data):
    stock_data = stock_data[['Date', 'Close', 'Changes']]
    final_data = sentiment_data.merge(stock_data, left_on='Date', right_on='Date')
    final_data = final_data.rename(index=str, columns={-1: 'Negative', 0: 'Neutral', 1: 'Positive'})

    # Remove NaNs
    final_data = final_data[final_data['Changes'] == final_data['Changes']]
    final_data.to_csv('../data/regressor_data.csv')
    return final_data

if __name__ == '__main__':
    tesla_data = google_stocks('TSLA', shiftby=3, startdate=(11, 28, 2017), enddate=(12, 11, 2017))
    sentiment_data = get_sentiment_data('../data/tweets_classifed_using_classifier.csv')

    # print(tesla_data)

    final_data = get_final_data(sentiment_data, tesla_data)

    # Build the regressor
    y = final_data['Changes']
    X = final_data[['Positive', 'Neutral', 'Negative']]
    # print(final_data)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

    regressor = LinearRegression()
    regressor.fit(X_train, y_train)

    x_plot = final_data['Date']
    y_pred = regressor.predict(X)
    y_true = y

    # line1, = plt.plot(x_plot, y_pred, label="Predicted")
    # line2, = plt.plot(x_plot, y_true, label="Actual")
    # plt.ylabel("3-day Change in Stock Price ($)")
    # plt.title("Regressor Results on $TSLA Stock Data")
    # plt.legend(handles=[line1, line2])
    # plt.grid()
    # plt.show()

    # print(final_data)
    # print(X_test)
    # print("Correlation (r2 score): ")
    # print(regressor.score(X_test, y_test))
    # print(regressor.predict(X_test))
    # print(y_test)
    # print("Regressor weights:")
    # print(regressor.coef_)
