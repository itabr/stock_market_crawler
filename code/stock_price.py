import pandas as pd
import io
import requests
import time
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
 
def google_stocks(symbol, startdate = (1, 1, 2006), enddate = None):
 
    startdate = str(startdate[0]) + '+' + str(startdate[1]) + '+' + str(startdate[2])
 
    if not enddate:
        enddate = time.strftime("%m+%d+%Y")
    else:
        enddate = str(enddate[0]) + '+' + str(enddate[1]) + '+' + str(enddate[2])

    stock_url = "http://finance.google.com/finance/historical?q=" + symbol + \
                "&startdate=" + startdate + "&enddate=" + enddate + "&output=csv"

    print stock_url
 
    raw_response = requests.get(stock_url).content
    
    stock_data = pd.read_csv(io.StringIO(raw_response.decode('utf-8')))
    stock_data['Date'] = stock_data['Date'].apply(lambda x: datetime.strptime(x, '%d-%b-%y').date())
    # stock_data['Date'] = stock_data['Date'].apply(lambda x: str(x))
    return stock_data

if __name__ == '__main__':
    tesla_data = google_stocks('TSLA', startdate=(11, 28, 2017), enddate=(12, 11, 2017))
    tesla_data = tesla_data[['Date', 'Close']]
    # For a given data, this is tomorrow's stock price - today's
    # Do this since tweets likely show effect in the future
    tesla_data['Changes'] = tesla_data['Close'] - tesla_data['Close'].shift(-1)

    sentiment_data = pd.read_csv('tweets_classifed_using_classifier.csv')
    sentiment_data.columns = ['Classification', 'Date', 'Tweet']
    sentiment_data = sentiment_data.drop('Tweet', axis=1)

    for index, row in sentiment_data.iterrows():
        datestring = row['Date'][4:10] + " " + row['Date'][-4:]
        datetime_object = datetime.strptime(datestring, '%b %d %Y')
        sentiment_data.at[index, 'Date'] = datetime_object.date()

    sentiment_data_count = pd.DataFrame({'count' : sentiment_data.groupby( [ "Date", "Classification"] ).size()}).reset_index()
    sentiment_data_count = sentiment_data_count.pivot(index='Date', columns='Classification', values='count').reset_index()

    # print(sentiment_data_count.merge(tesla_data, left_on='Date', right_on='Date'))
    final_data = sentiment_data_count.merge(tesla_data, left_on='Date', right_on='Date')
    final_data = final_data.rename(index=str, columns={-1: 'Negative', 0: 'Neutral', 1: 'Positive'})

    # removes NaN values
    final_data = final_data[final_data['Changes'] == final_data['Changes']]
    print(final_data)

    # Build the regressor
    y = final_data['Changes']
    X = final_data[['Positive', 'Neutral', 'Negative']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    print(regressor.score(X_test, y_test))






