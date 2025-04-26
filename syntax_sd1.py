# 1. Basic For Loop with Conditionals
numbers = [3, 6, 9, 12, 15]

for num in numbers:
    if num % 2 == 0:
        print(f"{num} is even")
    else:
        print(f"{num} is odd")

print("-" * 30)

# 2. Function with Return Value
def square(number):
    return number * number

result = square(7)
print("The square is:", result)

print("-" * 30)

# 3. Dictionary Lookup
user_ages = {"Alice": 30, "Bob": 25, "Charlie": 35}

name = "Bob"

if name in user_ages:
    print(f"{name} is {user_ages[name]} years old.")
else:
    print(f"{name} not found.")

print("-" * 30)

# 4. List Comprehension
squares = [x**2 for x in range(5)]
print("Squares from 0 to 4:", squares)

print("-" * 30)

# 5. Open and Read a File (requires sample.txt to exist)
try:
    with open("sample.txt", "r") as file:
        for line in file:
            print(line.strip())
except FileNotFoundError:
    print("sample.txt not found. Skipping file read.")

print("-" * 30)

# 6. Try-Except Block
try:
    result = 10 / 0
except ZeroDivisionError:
    print("You can't divide by zero.")

print("-" * 30)

# 7. While Loop with Break
counter = 0

while True:
    print("Counting:", counter)
    counter += 1
    if counter == 5:
        break

print("-" * 30)