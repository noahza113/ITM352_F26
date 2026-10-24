# Read taxi_1000.csv and calculate the total and average fare, plus the
# maximum trip distance, for trips with fares greater than $10.
import csv

filename = "..\\taxi_1000.csv"

with open(filename, 'r') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)

    total_fare = 0.0
    max_distance = 0.0
    average_fare = 0.0
    qualifying_trips = 0

    fare_index = header.index('Fare')
    distance_index = header.index('Trip Miles')

    for row in csv_reader:
        fare = float(row[fare_index])
        if fare > 10:
            distance = float(row[distance_index])

            total_fare += fare
            if distance > max_distance:
                max_distance = distance
            qualifying_trips += 1

if qualifying_trips > 0:
    average_fare = total_fare / qualifying_trips

print(f"Total Fare: ${total_fare:.2f}")
print(f"Average Fare: ${average_fare:.2f}")
print(f"Max Trip Distance: {max_distance:.2f} miles")