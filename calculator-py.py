import os

# This function adds two numbers
def add (x, y):
    return x + y

# This function subtracts two numbers
def subtract (x, y):
    return x - y

#This function multiplies two numbers
def multiply (x, y):
    return x * y

#This function divides two numbers
def divide (x, y):
    return x / y

while True:
    # clear the screen
    os.system('cls')
    # print menu and then take input form the user
    
    print("Select Operation.")
    print("1.Add")
    print("2.Subtract")
    print("3.Multiply")
    print("4.Divide")
    choice = input("Enter choice(1/2/3/4): ")

    # check if choice is one of the options
    if choice in ('1', '2', '3', '4'):
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        if choice == '1':
            print(num1, "+", num2, "=", add(num1, num2))
            print("wow you have ", add(num1, num2), " of... something.")

        elif choice == '2':
            print(num1, "-", num2, "=", subtract(num1, num2))
            print("sooo... you have ", subtract(num1, num2), " almost out!!")

        elif choice == '3':
            print(num1, "*", num2, "=", multiply(num1, num2))
            print("with ", multiply(num1, num2), ", you have bunches and bunches... clearly")

        elif choice == '4':
            print(num1, "/", num2, "=", divide(num1, num2))
            print("dividing and conquering has given us ", divide(num1, num2), "!" )

        # check if user wants another calculation
        # break the while loop if answer is no
        next_calculation = input("Let's do next calculation? (yes/no): ")
        if next_calculation == "no":
            break
    else:
        print("Invalid Input")