# Python Quest: The support desk
# Build a support-cost calculator. Read service then hours on separate lines. Rates: basic = 10, urgent = 20. Normalize the service. Check service first: unknown service → Unknown service. Otherwise convert hours to float: invalid or negative hours → Invalid hours. For valid input, print Total: AMOUNT with two decimal places. Put the calculation in a function named calculate_total(rate, hours).
# Run with: python3 10_final_mission.py

def calculate_total(rate, hours):
    return rate * hours

rates = {"basic": 10, "urgent": 20}
service = input().strip().lower()
hours_text = input()
if service not in rates:
    print("Unknown service")
else:
    try:
        hours = float(hours_text)
        if hours < 0:
            print("Invalid hours")
        else:
            total = calculate_total(rates[service], hours)
            print(f"Total: {total:.2f}")
    except ValueError:
        print("Invalid hours")
