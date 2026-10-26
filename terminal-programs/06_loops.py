# Python Quest: Repeat with purpose
# Read a non-negative integer n. Use a loop to add the integers from 1 through n, including n. Print only the final total. When n is 0, print 0.
# Run with: python3 06_loops.py

n = int(input())
total = 0
for number in range(1, n + 1):
    total = total + number
print(total)
