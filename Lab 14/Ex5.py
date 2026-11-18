#Get a JSON file from City of Chicago's data portal and ayalzye driver types
import pandas as pd
import requests

url = "https://data.cityofchicago.org/resource/97wa-y6ff.json?$select=driver_type,count(license)&$group=driver_type"
response = requests.get(url)

response_json = response.json()

print ("Driver Type and counts:")
print(response_json)

reponse_df = pd.DataFrame(response_json)
reponse_df.columns = ["driver_type", "count"]
reponse_df = reponse_df.set_index("driver_type")
print(reponse_df)