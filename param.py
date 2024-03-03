import pandas as pd
from pmdarima import auto_arima
import json

# Load the training dataset
train_df = pd.read_csv('train_data.csv')

# Initialize a dictionary to store ARIMA parameters for each product
arima_params = {}

# Loop through each product in the training dataset to fit an auto_arima model
for product in train_df['Product_Code'].unique():
    product_series = train_df[train_df['Product_Code'] == product]['Sales']
    auto_arima_model = auto_arima(product_series, start_p=0, start_q=0, max_p=2, max_q=2, m=1,
                                  seasonal=False, stepwise=True, trace=True,
                                  error_action='ignore', suppress_warnings=True)
                                  
    # Store the optimal parameters (p, d, q)
    arima_params[product] = auto_arima_model.order

# Save the ARIMA parameters to a JSON file
with open('arima_params.json', 'w') as file:
    json.dump(arima_params, file)
