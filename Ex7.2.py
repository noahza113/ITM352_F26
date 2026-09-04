#This program converts a temperature from Fahrenheit to Celsius
#Create the conversion as a function
#Name: Noah Zane
#Date: 9/4/2026


def F_to_C(Fahrenheit):
    Celsius = (Fahrenheit - 32) * 5/9
    rounded_Celsius = round(Celsius, 2)
    return rounded_Celsius

Fahrenheit_input = input("Enter temperature in Fahrenheit: ")
Fahrenheit_float = float(Fahrenheit_input)

Celsius_value = F_to_C(Fahrenheit_float)

print("You entered:", Fahrenheit_float)
print("The temperature in Celsius is:", Celsius_value)
