#This programs prompts the user to enter a weight in pounds and then converts that weight to kilograms and displays the result.
#Name: Noah Zane
#Date: 9/4/2026

#print("The weight in Kilograms is:", float(input("Enter Weight in pounds: ")) * (0.453592))

KG_to_Pounds = 0.453592
Weight_in_pounds = input("Enter Weight in pounds: ")
Weight_in_pounds_float = float(Weight_in_pounds)
Weight_in_KG = Weight_in_pounds_float * KG_to_Pounds

print("The weight in pounds is:", Weight_in_pounds_float)
print("The weight in Kilograms is:", Weight_in_KG)
