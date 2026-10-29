
operator = input("What operator would you like to use?(+, _, *, /): ")
num1= float(input("Enter the first number: "))
num2= float(input("Enter the second number: "))

total = num1 + num2

if operator == "+":
    result = num1 + num2
    print(round(result, 3))
elif operator == "-":
    result = num1 - num2
    print(round(result, 3))
elif operator == "*":
    result = num1 * num2
    print(round(result, 3))
elif operator == "/":
    result = num1 / num2
    print(round(result, 3))

