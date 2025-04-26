def calculator():
    while True:
        print("Simple Calculator")
        print("Choose an operation")
        print("1. Addition ")
        print("2. Subtraction")
        print("3 Multiplication")
        print("4. Division")
        print("5. Exit")

        choice = input("Enter the number of operation 1-5")

        if choice == '5':
            print("Exiting the calculator. Goodbye!")
            break

        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Enter the first number:"))
                num2 = float(input("Enter the second number:"))

                if choice == '1':
                    result = num1 + num2
                    
                elif choice == '2':
                    result = num1 - num2
                    
                elif choice  == '3':
                    result = num1 * num2 
                    
                elif choice == '4':
                    if num2 != 0:
                            result = num1 / num2
                            
                    else:
                            print("Error: Division by zero is not allowed.")
                            continue
                
                print(f"The result is {result}")
            
            except ValueError:
                print("Invalid input. Please enter numeric values.")
        else:
            print("Invalid choice . Please select a valid option.")
            
# Run the calculator
calculator()