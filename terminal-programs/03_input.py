# Python Quest: Meet your user
# Read a name on the first line and an age on the second. Print: NAME will be AGE_NEXT next year. For inputs Maya and 24, print Maya will be 25 next year. Do not print input prompts in assessed challenges.
# Run with: python3 03_input.py

name = input()
age = int(input())
print(f"{name} will be {age + 1} next year")
