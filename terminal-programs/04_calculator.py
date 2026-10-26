# Python Quest: Split the bill
# Read bill amount, tip percentage, and number of people on three lines. Add the tip, divide the total equally, and print Each pays: AMOUNT with two decimal places. Assume people is positive.
# Run with: python3 04_calculator.py

bill = float(input())
tip_percent = float(input())
people = int(input())
total = bill + bill * tip_percent / 100
print(f"Each pays: {total / people:.2f}")
