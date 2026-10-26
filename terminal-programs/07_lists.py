# Python Quest: Keep an inventory
# Read one line of comma-separated inventory names. Print Items: COUNT, followed by each name on a new line prefixed with - and a space. Strip spaces from each name. Assume there is at least one non-empty name.
# Run with: python3 07_lists.py

items = input().split(",")
print(f"Items: {len(items)}")
for item in items:
    print(f"- {item.strip()}")
