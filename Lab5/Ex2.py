
Trip_durations = (1.1, 0.8, 2.5, 2.6)
Trip_fares = ("$6.25", "$5.25", "$10.50", "$8.05")

trips = {
    "miles": Trip_durations,
    "fares": Trip_fares,
}


print(trips)
print("Duration of the third trip is:", trips["durations"][2], "durations")
print("The fare of the third trip is:", trips["fares"][2], "fare")
