# Basic calculator program with repeated calculations


def calculate(num1, num2, choice):
    if choice == "1":
        return num1 + num2
    elif choice == "2":
        return num1 - num2
    elif choice == "3":
        return num1 * num2
    elif choice == "4":
        if num2 == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return num1 / num2
    raise ValueError("Invalid operation selected.")


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
        result = calculate(num1, num2, choice)
    except ValueError:
        print("Error: Please enter valid numbers.")
        continue
    except ZeroDivisionError as exc:
        print(f"Error: {exc}")

        again = input("Would you like to calculate again? (y/n): ").strip().lower()
        while again not in ("y", "n"):
            print("Please enter 'y' or 'n'.")
            again = input("Would you like to calculate again? (y/n): ").strip().lower()

        if again != "y":
            print("Goodbye!")
            break
        continue

    print(f"Result: {num1} + {num2} = {result}" if choice == "1" else
          f"Result: {num1} - {num2} = {result}" if choice == "2" else
          f"Result: {num1} * {num2} = {result}" if choice == "3" else
          f"Result: {num1} / {num2} = {result}")

    again = input("Would you like to calculate again? (y/n): ").strip().lower()
    while again not in ("y", "n"):
        print("Please enter 'y' or 'n'.")
        again = input("Would you like to calculate again? (y/n): ").strip().lower()

    if again != "y":
        print("Goodbye!")
        break
