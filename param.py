import pandas as pd
from pmdarima import auto_arima
import json

train_df = pd.read_csv('train_data.csv')

arima_params = {}


for product in train_df['Product_Code'].unique():
    product_series = train_df[train_df['Product_Code'] == product]['Sales']
    auto_arima_model = auto_arima(product_series, start_p=0, start_q=0, max_p=2, max_q=2, m=1,
                                  seasonal=False, stepwise=True, trace=True,
                                  error_action='ignore', suppress_warnings=True)
                                  
    
    arima_params[product] = auto_arima_model.order

with open('arima_params.json', 'w') as file:
    json.dump(arima_params, file)
