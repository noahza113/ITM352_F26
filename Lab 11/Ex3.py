#Create a DataFrame from a csv file and create a pivot table aggregating sales by region and order_type
#Name: Noah Zane
#Date: Oct. 30,2026

import pandas as pd
import numpy as np
import ssl

# Ignore SSL certificate errors
ssl._create_default_https_context = ssl._create_unverified_context
# Tell Pandas to print all columns when displaying a DataFrame
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format',{:.2f},format)#Forat float num

csv_file = 'https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K&export=download'

try:
    df = pd.read_csv(csv_file,engine='pyarrow',on_bad_lines='skip')
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    print(df.head())

    #Calculate sales total per row
    df['sales'] = df['quantity'] * df['unit_price']

    # Create a pivot table aggregating sales by region and order type
    pivot_table = pd.pivot_table(df,
                                values='sales',
                                index='customer_state',
                                columns=('order_type''order_type'),
                                aggfunc='mean',
                                margins=True,
                                margins_name='Total Sales')
    print(pivot_table)

except Exception as e:
    print(f"Error occurred while reading the CSV file: {e}")