from flask import Flask
from flask import request
from http.client import responses
import statistics as st
import json
import pandas as pd
import math


app = Flask(__name__)

gold_df = pd.read_csv('gold-historical-data.csv')
silver_df = pd.read_csv('silver-historical-data.csv')

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/commodity', methods = ['GET'])
def commodity_search():
    if request.method == 'GET':
        start_date = request.values.get('start_date')
        end_date = request.values.get('end_date')
        commodity_type = request.values.get('commodity_type')
        print(start_date)
        print(end_date)
        print(commodity_type)
        
        if commodity_type == 'gold':
            df = gold_df
        elif commodity_type == 'silver':
            df = silver_df

        df['Date'] = pd.to_datetime(df['Date'])  
        mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
        target_sub_df = df.loc[mask]
        # print(target_sub_df)

        target_dates = target_sub_df['Date'].tolist()
        target_prices = target_sub_df['Price'].tolist()
        target_size = len(target_dates)
        
        data = {}
        for i in range(target_size):
            data[str(target_dates[i].date())] = target_prices[i]

        return_obj = {
            "data": data,
            "mean": round(st.mean(target_prices), 2),
            "variance": round(st.variance(target_prices), 2)
        }

        return json.dumps(return_obj)
    else:
        return responses[405]


if __name__ == '__main__':
   app.run(debug=True, host='0.0.0.0', port=8080)