# Python Quest: Triage the ticket
# Read a severity level. Ignore surrounding spaces and letter case. Print Urgent for high, Normal for medium, and Low for any other value.
# Run with: python3 05_decisions.py

severity = input().strip().lower()
if severity == "high":
    print("Urgent")
elif severity == "medium":
    print("Normal")
else:
    print("Low")
