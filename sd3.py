# Basic Python Commands

# 1. Print statement
print("Hello, World!")

# 2. Variables and types
a = 10              # Integer
b = 3.14            # Float
c = "Python"        # String
d = True            # Boolean

# 3. List (Mutable, ordered collection of items)
my_list = [1, 2, 3, 4, 5]

# 4. Dictionary (Key-value pairs)
my_dict = {"name": "Alice", "age": 25, "city": "New York"}

# 5. Conditional statements (if-else)
x = 5
if x > 3:
    print("x is greater than 3")
else:
    print("x is not greater than 3")

# 6. Loops (for and while)
# For loop
for i in range(5):
    print(i)

# While loop
count = 0
while count < 5:
    print(count)
    count += 1

# 7. Functions
def greet(name):
    return f"Hello, {name}!"

# Calling the function
greeting = greet("Bob")
print(greeting)

# 8. Classes and Objects
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"My name is {self.name} and I am {self.age} years old."

# Creating an object
person1 = Person("John", 30)
print(person1.introduce())

# 9. File Handling
# Writing to a file
with open("example.txt", "w") as file:
    file.write("This is a test file.")

# Reading from a file
with open("example.txt", "r") as file:
    content = file.read()
    print(content)

# 10. Exception Handling
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
