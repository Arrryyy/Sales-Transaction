import pandas as pd
import matplotlib.pyplot as plt
from forecasting import forecast_sales
import json
# Load the datasets
train_df = pd.read_csv('train_data.csv')
test_df = pd.read_csv('test_data.csv')

# Load ARIMA parameters from JSON file
with open('arima_params.json', 'r') as file:
    arima_params = json.load(file)

def recommend_best_product(train_df, test_df, arima_params, desired_sales, investment_period):
    # Step 2: Forecasting
    forecasts = {}
    for product, params in arima_params.items():
        forecast, weeks = forecast_sales(product, params, train_df, test_df, period=investment_period)
        total_forecasted_sales = sum(forecast)
        forecasts[product] = (total_forecasted_sales, weeks, forecast)
    
    # Step 3: Identifying the Best Product
    best_product = max(forecasts.items(), key=lambda x: x[1][0] if x[1][0] >= desired_sales else -1)
    
    # Step 4: Finding Close Alternatives
    alternatives = sorted(forecasts.items(), key=lambda x: abs(desired_sales - x[1][0]))[:6]
    
    # Step 5: Plotting
    plt.figure(figsize=(12, 8))
    for product, details in alternatives:
        weeks, forecast = details[1], details[2]
        plt.plot(weeks, forecast, label=f'{product} Forecast')
    
    plt.title('Top Investment Products Forecast')
    plt.xlabel('Week')
    plt.ylabel('Forecasted Sales')
    plt.legend()
    plt.show()
    
    # Recommendation Output
    print(f"The best product for investment is: {best_product[0]} with forecasted sales of {best_product[1][0]}")
    print("Top alternatives include:", ", ".join([prod[0] for prod in alternatives if prod[0] != best_product[0]]))


desired_sales = int(input("Enter the desired number of sales: "))
investment_period = int(input("Enter the investment period in weeks: "))
recommend_best_product(train_df, test_df, arima_params, desired_sales, investment_period)
