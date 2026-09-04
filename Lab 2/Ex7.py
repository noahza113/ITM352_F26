#This program converts a temperature from Fahrenheit to Celsius.
#Name: Noah Zane
#Date: 9/4/2026


Fahrenheit_input = input("Enter temperature in Fahrenheit: ")
Fahrenheit_float = float(Fahrenheit_input)

Celsius_value = (Fahrenheit_float - 32) * 5/9
Celsius_value = round(Celsius_value, 2)

print("You entered:", Fahrenheit_float)
print("The temperature in Celsius is:", Celsius_value)
