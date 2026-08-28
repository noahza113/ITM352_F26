# Basic calculator program with repeated calculations

while True:
    print("\nSimple Calculator")
    print("Choose an operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("q. Quit")

    choice = input("Enter your choice (1/2/3/4/q): ")

    if choice.lower() == "q":
        print("Goodbye!")
        break

    if choice not in ("1", "2", "3", "4"):
        print("Invalid operation selected.")
        continue

    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
    except ValueError:
        print("Error: Please enter valid numbers.")
        continue

    if choice == "1":
        result = num1 + num2
        print(f"Result: {num1} + {num2} = {result}")
    elif choice == "2":
        result = num1 - num2
        print(f"Result: {num1} - {num2} = {result}")
    elif choice == "3":
        result = num1 * num2
        print(f"Result: {num1} * {num2} = {result}")
    elif choice == "4":
        if num2 == 0:
            print("Error: Division by zero is not allowed.")
        else:
            result = num1 / num2
            print(f"Result: {num1} / {num2} = {result}")

    again = input("Would you like to calculate again? (y/n): ")
    if again.lower() != "y":
        print("Goodbye!")
        break
