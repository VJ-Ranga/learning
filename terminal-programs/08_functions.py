# Python Quest: Build a reusable tool
# Define a function celsius_to_fahrenheit(celsius) that returns celsius * 9 / 5 + 32. Read a temperature, call your function, and print the result with one decimal place followed by a space and F.
# Run with: python3 08_functions.py

def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32

temperature = float(input())
result = celsius_to_fahrenheit(temperature)
print(f"{result:.1f} F")
