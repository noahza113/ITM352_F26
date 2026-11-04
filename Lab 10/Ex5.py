import pandas as pd

homes_data_file = "https://drive.google.com/uc?export=download&id=1M-X_bypJJ6K5p6eM6aYBwt1qIizIiIex"
homes_df = pd.read_csv(homes_data_file)
print(homes_df.head())

#Print the dimensions of the dataframe
shape = homes_df.shape
print("The dimensions of the dataframe are:", shape)

df_big = homes_df[homes_df['units'] >= 500]
print(df_big.head(10))

#Look at data types
print(df_big.info())

#Corce land_sqft, gross_sqft, and sale_price to numric
df_big['land_sqft'] = pd.to_numeric(df_big['land_sqft'], errors=coerce)
df_big['gross_sqft'] = pd.to_numeric(df_big['gross_sqft'], errors=coerce)
df_big['sale_price'] = pd.to_numeric(df_big['sale_price'], errors=coerce)

#Look at the datatypes and print the clened data
print("After cleaning...")
print(df_big.info())
print(df_big.head(10))

#We have some null values. Drop these.
df_big = df_big.dropna()

#Now drop duplicate records. 
df_big = df_big.drop_duplicates()

#filter out 0 sales
df_big = df_big(('sales_price') > 0)
