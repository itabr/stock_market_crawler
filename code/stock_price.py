import pandas as pd
import io
import requests
import time
from datetime import datetime
 
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
    return stock_data

if __name__ == '__main__':
    tesla_data = google_stocks('TSLA', startdate=(11, 26, 2017), enddate=(12, 9, 2017))
    tesla_data = tesla_data[['Date', 'Close']]
    tesla_data['diff Close'] = tesla_data['Close'] - tesla_data['Close'].shift(-1)
    print(tesla_data)
