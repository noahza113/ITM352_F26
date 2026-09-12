import from HandyMath import max, min

# Get 2 numbers from the user for the HandyMath calculations 
number1 = float(input("Enter the first number: "))
number2 = float(input("Enter the second number: "))

#Display the results of the HandyMath calculations
print("The midpoint of", number1, "and", number2, "is:", HandyMath.midpoint(number1, number2))
print("The square root of", number1, "is:", HandyMath.squareroot(number1))
print("The square root of", number2, "is:", HandyMath.squareroot(number2))
print("The maximum of", number1, "and", number2, "is:", HandyMath.max(number1, number2))
print("The minimum of", number1, "and", number2, "is:", HandyMath.min(number1, number2))
print("The exponent of", number1, "raised to the power of", number2, "is:", HandyMath.exponent(number1, number2))
