# Ask the user to enter a decimal number. Calculate the square root of that number, round it to
# two decimal places, and print it out.
# Name: Noah Zane
# Date: 9/2/2026

input_value = input ("Enter a floating point number: ")
float_value = float(input_value)
square_value = float_value ** 2
round_value = round(square_value, 2)

print("You entered:", float_value)
print("The square of the number you entered is:", round_value, "Have a nice day!")