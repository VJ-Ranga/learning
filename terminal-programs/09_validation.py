# Python Quest: Handle the unexpected
# Read an integer quantity. Print Quantity: N when it is zero or positive, Quantity cannot be negative for a negative integer, and Enter a whole number for invalid text.
# Run with: python3 09_validation.py

try:
    quantity = int(input())
    if quantity < 0:
        print("Quantity cannot be negative")
    else:
        print(f"Quantity: {quantity}")
except ValueError:
    print("Enter a whole number")
