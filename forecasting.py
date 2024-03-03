import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import json

# Assuming 'train_data.csv' and 'test_data.csv' are in the current directory
train_df = pd.read_csv('train_data.csv')
test_df = pd.read_csv('test_data.csv')

# Load ARIMA parameters
with open('arima_params.json', 'r') as file:
    arima_params = json.load(file)

def forecast_sales(product_code, params, train_df, test_df):
    test_data_for_product = test_df[test_df['Product_Code'] == product_code]
    if test_data_for_product.empty:
        print(f"No test data for product code {product_code}, cannot forecast.")
        return None
    
    forecasting_steps = len(test_data_for_product)
    print(f"Forecasting for {forecasting_steps} weeks.")

    product_series = train_df[train_df['Product_Code'] == product_code]['Sales']
    if product_series.empty:
        print(f"No training data for product code {product_code}, cannot forecast.")
        return None

    model = ARIMA(product_series, order=(params[0], params[1], params[2]))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecasting_steps)
    
    return forecast, test_data_for_product['Week'].tolist()

product_code = 'P1'  # Example product code
if product_code in arima_params:
    params = arima_params[product_code]
    forecast, weeks = forecast_sales(product_code, params, train_df, test_df)
    if forecast is not None:
        plt.figure(figsize=(10, 6))
        actual = test_df[test_df['Product_Code'] == product_code]['Sales']
        plt.plot(weeks, actual, label='Actual Sales')
        plt.plot(weeks, forecast, color='red', label='Forecasted Sales')
        plt.title(f'Sales Forecast vs Actual for Product {product_code}')
        plt.xlabel('Week')
        plt.ylabel('Sales')
        plt.xticks(rotation=45)  
        plt.legend()
        plt.show()
else:
    print(f"No parameters found for {product_code}")
