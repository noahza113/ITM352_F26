#Simple dictionary sample

Country_capitals = {
    "Germany": {"capital": "Berlin", "population": 3769000},
    "Canada": {"capital": "Ottawa", "population": 1017449},
    "France": {"capital": "Paris", "population": 2161000}
}

print("Country Capitals:", Country_capitals)
print(Country_capitals["Canada"]["capital"])
print(Country_capitals["Canada"]["population"])

Country_capitals["England"] = {"capital": "London", "population": 8982000}
print(Country_capitals["England"]["capital"])
print(Country_capitals["England"]["population"])

