import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget
from PyQt6.QtChart import QChart, QChartView, QLineSeries
from PyQt6.QtCore import Qt
import pandas as pd
import json
from statsmodels.tsa.arima.model import ARIMA
# Assuming forecasting.py is in the same directory and contains the forecast_sales function
from forecasting import forecast_sales

class ForecastingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Forecasting")
        self.setGeometry(100, 100, 800, 600)
        
        # UI Components
        self.productCodeInput = QLineEdit(self)
        self.productCodeInput.setPlaceholderText("Enter Product Code")
        self.forecastButton = QPushButton("Forecast", self)
        self.forecastButton.clicked.connect(self.on_forecast_clicked)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.productCodeInput)
        layout.addWidget(self.forecastButton)
        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def on_forecast_clicked(self):
        product_code = self.productCodeInput.text()
        # Load data and ARIMA parameters
        train_df = pd.read_csv('train_data.csv')
        test_df = pd.read_csv('test_data.csv')
        with open('arima_params.json', 'r') as file:
            arima_params = json.load(file)
        
        if product_code in arima_params:
            params = arima_params[product_code]
            forecast, weeks = forecast_sales(product_code, params, train_df, test_df)
            # Display results on the chart
            self.display_forecast_chart(forecast, weeks)
        else:
            print("Product code not found in ARIMA parameters.")

    def display_forecast_chart(self, forecast, weeks):
        series = QLineSeries()
        for week, value in zip(weeks, forecast):
            series.append(week, value)
        
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Forecasted Sales")
        chartView = QChartView(chart)
        self.setCentralWidget(chartView)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = ForecastingApp()
    mainWindow.show()
    sys.exit(app.exec())
