import os
import json
import re

# 1. OS and File Handling: List files in the current directory
print("1. OS and File Handling: Listing files in the current directory")
files = os.listdir('.')  # lists files in the current directory
for file in files:
    print(file)
print("-" * 30)

# 2. Classes & Objects: A simple Person class
print("2. Classes & Objects: Creating and using a Person class")
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hi, my name is {self.name} and I am {self.age} years old."

person1 = Person("Alice", 30)
print(person1.greet())
print("-" * 30)

# 3. Parsing JSON: Parse a JSON string and print its key-value pairs
print("3. Parsing JSON: Parsing a JSON string")
json_str = '{"name": "Bob", "age": 25, "city": "New York"}'
data = json.loads(json_str)
print("Parsed JSON data:")
for key, value in data.items():
    print(f"{key}: {value}")
print("-" * 30)

# 4. Nested Loops: Create a simple multiplication table (1 to 3)
print("4. Nested Loops: Multiplication table (1-3)")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i} x {j} = {i * j}", end="\t")
    print()  # New line after each row of the table
print("-" * 30)

# 5. Regex: Find all words that start with 'a' (case-insensitive) in a sentence
print("5. Regex: Finding words that start with 'a'")
text = "An apple a day keeps the doctor away, and always a good start."
matches = re.findall(r'\ba\w*', text, re.IGNORECASE)
print("Words starting with 'a':", matches)
print("-" * 30)

# 6. User Input: Simulated user input example (interactive input is commented out)
print("6. User Input: Simulated user input example")
# Uncomment the lines below to enable interactive input:
# user_response = input("Enter your favorite programming language: ")
# print(f"You said: {user_response}")
# For demonstration, we'll simulate the user input:
user_response = "Python"
print(f"You said: {user_response}")
print("-" * 30)
