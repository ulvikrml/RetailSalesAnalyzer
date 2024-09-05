import pandas as pd
import math
import matplotlib.pyplot as plt

class RetailSalesAnalyzer:
    def __init__(self):
        self.data = pd.read_csv("retail_sales_dataset.csv")
        self.data['Date'] = pd.to_datetime(self.data['Date'])
    def clean(self):
        # self.data['Price per Unit'].fillna(self.data['Total Amount']/self.data['Quantity'], inplace=True)
        self.data['Price per Unit'] = self.data['Price per Unit'].fillna(
            self.data['Total Amount']/self.data['Quantity']
        )
        self.data['Total Amount'].fillna(self.data['Price per Unit']/self.data['Quantity'], inplace=True)
        self.data['Quantity'].fillna(self.data['Total Amount']/self.data['Price per Unit'], inplace=True)
        self.data['Gender'].fillna('Unknown', inplace=True)
        self.data.dropna(inplace=True)

    def total_sales_per_product(self):
        return self.data.groupby('Product Category')['Total Amount'].sum()
    def best_selling_product(self):
        return self.total_sales_per_product().sort_values(ascending=False).index[0]
    def average_daily_sales(self):
        daily_sales = self.data.groupby(self.data['Date'].dt.date)['Total Amount'].sum()
        return math.ceil(daily_sales.mean())

    def plot_sales_trend(self):
        self.data.groupby('Date')['Total Amount'].sum().plot(kind='line')
        plt.title('Sales Trend Over Time')
        plt.xlabel('Date')
        plt.ylabel('Total Sales')
        plt.show()

    def plot_sales_per_product(self):
        self.total_sales_per_product().plot(kind='bar')
        plt.title('Sales Per Product Category')
        plt.xlabel('Category')
        plt.ylabel('Total Sales')
        plt.show()

analyzer = RetailSalesAnalyzer()
analyzer.clean()
print('Total Data\n',analyzer.data.head(10))
print('Total Sales Per Product Category\n',analyzer.total_sales_per_product())
print('Best Selling Category: ',analyzer.best_selling_product())
print('Average Daily Total Sales\n',analyzer.average_daily_sales())
print(analyzer.plot_sales_trend())
print(analyzer.plot_sales_per_product())