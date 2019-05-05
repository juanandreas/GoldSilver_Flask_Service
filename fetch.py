import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

user_auth = {'User-Agent': 'Mozilla/5.0'}

def html_to_text(html_arr):
    return list(map(lambda x: x.text, html_arr))

def str_date_to_datetime(date):
    date_tm = datetime.strptime(date, '%b %d, %Y')
    return str(date_tm.date())

def extract_data_to_csv(url):
    data_name = url.split('/')[-1]
    response = requests.get(url, headers=user_auth)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find_all('table', class_="genTbl closedTbl historicalTbl", id="curr_table" )[0]

    dates_col = []
    historical_prices_col = []
    for i, row in enumerate(table.find_all('tr'), 0):
        if i == 0:
            # schema
            schema_arr = html_to_text(table.find_all('th'))[:2]
        else:
            # data
            html_data_arr = row.find_all('td')
            data_arr = html_to_text(html_data_arr)
            date = str_date_to_datetime(data_arr[0])
            historical_price = float(data_arr[1].replace(',',''))
            dates_col.append(date)
            historical_prices_col.append(historical_price)

    # print(schema_arr)
    # print(dates_col)

    d = {}
    d[schema_arr[0]] = dates_col
    d[schema_arr[1]] = historical_prices_col

    df = pd.DataFrame(data=d)
    # print(df)
    df.to_csv('{}.csv'.format(data_name), index=None, header=True)


if __name__ == "__main__":
    gold_url = 'https://www.investing.com/commodities/gold-historical-data'
    silver_url = 'https://www.investing.com/commodities/silver-historical-data'
    extract_data_to_csv(gold_url)
    extract_data_to_csv(silver_url)
