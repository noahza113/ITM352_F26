# This program will ask the user to enter a number between 1 and 100, then it will calculate the square of that number and display the result.
#Name: Noah Zane
#Date: 9/2/2026

value_entered = input("Enter a number between 1 and 100: ")
value_as_interger = int(value_entered)

valueSquared = value_as_interger ** 2

print("You enter:", value_as_interger)
print("The square of the number you entered is", valueSquared)

print("You entered:", value_entered, "and the square of", value_as_interger, "is:", valueSquared)