#Read a json file of taxi trip data and create a dataframe and some simple stats
import pandas as pd

#Read the JSON file into a DataFrame
df = pd.read_json("Taxi_Trips.json")

#Display the first few rows of the DataFrame
print(df.head())

#Display basic statstics about the dataframe
print(df.describe())

median = df["fare"].median()
print(f"The median fare value is:",median)