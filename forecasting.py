import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import json
import warnings
from statsmodels.tools.sm_exceptions import ValueWarning
from statsmodels.tools.sm_exceptions import ConvergenceWarning
warnings.simplefilter('ignore', ConvergenceWarning)
warnings.filterwarnings("ignore", category=ValueWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message="Non-stationary starting autoregressive parameters found.")
warnings.filterwarnings("ignore", message="Non-invertible starting MA parameters found.")
train_df = pd.read_csv('train_data.csv')
test_df = pd.read_csv('test_data.csv')


with open('arima_params.json', 'r') as file:
    arima_params = json.load(file)

def forecast_sales(product_code, params, train_df, test_df):
    test_data_for_product = test_df[test_df['Product_Code'] == product_code]
    if test_data_for_product.empty:
        print(f"No test data for product code {product_code}, cannot forecast.")
        return None
    
    forecasting_steps = len(test_data_for_product)
    # print(f"Forecasting for {forecasting_steps} weeks.")

    product_series = train_df[train_df['Product_Code'] == product_code]['Sales']
    if product_series.empty:
        # print(f"No training data for product code {product_code}, cannot forecast.")
        return None

    model = ARIMA(product_series, order=(params[0], params[1], params[2]))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=forecasting_steps)
    
    return forecast, test_data_for_product['Week'].tolist()

def calculate_accuracy_metric(forecast, actual):
    # Calculate Mean Absolute Error as an example
    if len(forecast) == 0 or len(actual) == 0:
        return float('inf')
    return sum(abs(forecast - actual)) / len(forecast)

def find_closest_product(train_df, test_df, arima_params):
    closest_product = None
    lowest_error = float('inf')
    for product_code, params in arima_params.items():
        forecast, week_indices = forecast_sales(product_code, params, train_df, test_df)
        if forecast is not None and len(week_indices) > 0:
            # Instead of using .iloc[], match 'Week' column in test_df with week_indices
            actual_sales = test_df[(test_df['Product_Code'] == product_code) & (test_df['Week'].isin(week_indices))]['Sales'].values
            # Ensure the length of forecast and actual_sales match before calculating error
            if len(forecast) == len(actual_sales):
                error = calculate_accuracy_metric(forecast, actual_sales)
                if error < lowest_error:
                    closest_product = product_code
                    lowest_error = error
    return closest_product, lowest_error

# Assuming train_df, test_df, and arima_params are already defined and loaded
closest_product, error = find_closest_product(train_df, test_df, arima_params)

def ask_print_closest_accurate_product(closest_product, error): 
    answer = input("Enter a 'Yes', to view the closest accurate product, or a 'No' to carry on: ").lower()
    if answer == "yes": 
        print(f"The closest product in terms of forecast accuracy is {closest_product} with an MAE of {error:.2f}")
    elif answer == "no": 
        pass
    else: 
        print("Wrong input! try again!")


def plot_forecast_vs_actual(train_df, test_df, arima_params):
    product_code = input("Enter a product code to forecast: ")  # Prompt the user for a product code
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
            print(f"Forecasting could not be performed for product code {product_code}.")
    else:
        print(f"No ARIMA parameters found for product code {product_code}.")
ask_print_closest_accurate_product(closest_product, error)
plot_forecast_vs_actual(train_df, test_df, arima_params)