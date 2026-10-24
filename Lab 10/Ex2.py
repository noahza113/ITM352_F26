#Create a pandas dataframe from individual lists.
#Do some simple tests on the data
import pandas as pd

#lists of individuals' names, ages, and genders

ages = [25, 30, 22, 35, 28, 40, 50, 18, 60, 45]
names = ["Joe", "Jaden", "Max", "Sidney", "Evgeni", "Taylor", "Pia", "Luis", "Blanca", "Cyndi"]
gender = ["M", "M", "M", "F", "M", "F", "F", "M", "F", "F"]

raw_data = zip(ages,gender)

#Create a Pandas dataframe from the lists
df = pd.dataframe()
