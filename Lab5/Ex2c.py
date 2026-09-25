
Trip_durations = (1.1, 0.8, 2.5, 2.6)
Trip_fares = ("$6.25", "$5.25", "$10.50", "$8.05")

trips = dict(zip(Trip_durations,Trip_fares))
print(trips)

trip_number = int(input("What trip do you want?"))

print("The duration of the trip is:", Trip_durations[trip_number - 1], "miles")
print("The fare of the trip is:", Trip_fares[trip_number - 1])