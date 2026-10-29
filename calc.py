
operator = input("Enter operator (+, -, /, *) ")

num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))

result = num1 + num2

if operator == "+":
    result = num1 + num2
    print(round(result, 3))
elif operator == "-":
    result = num1 - num2
    print(round(result, 3))
elif operator == "/":
    result = num1 / num2
    print(round(result, 3))
elif operator == "*":
    result = num1 * num2
    print(round(result, 3))
else:
    print(f"{operator} is not a valid operator")





