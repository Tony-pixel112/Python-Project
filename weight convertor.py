weight = float(input("Enter your weight: "))
unit = input("Enter kilograms or pounds: (K or L)")

if unit == "K":
    weight = weight * 2.205
    unit ="lbs."
elif unit == "L":
    weight = weight / 2.205
    unit = "kgs."
else:
    print(f"Bitch enter a valid unit damn ass!")

print(f"Your weight is {round(weight, 1)} {unit}")
