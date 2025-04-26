# 1. Class with Method and Object Instantiation
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        return f"{self.name} the {self.breed} says: Woof!"

my_dog = Dog("Rex", "Labrador")
print(my_dog.bark())

print("-" * 30)

# 2. Import from Module and Use a Function
import random

random_number = random.randint(1, 100)
print("Random number between 1 and 100:", random_number)

print("-" * 30)

# 3. Writing to a File
with open("output.txt", "w") as file:
    file.write("This file was created by Python.\n")
    file.write("You’re doing great!\n")

print("File written successfully.")

print("-" * 30)

# 4. Nested Loops with Conditionals
for i in range(1, 4):
    for j in range(1, 4):
        product = i * j
        print(f"{i} x {j} = {product}")
    print("--- End of inner loop ---")

print("-" * 30)

# 5. Function that Returns a Filtered List
def filter_even(numbers):
    return [num for num in numbers if num % 2 == 0]

original = [10, 15, 20, 25, 30]
evens = filter_even(original)
print("Even numbers:", evens)

print("-" * 30)

# 6. Use of enumerate() to Track Index
fruits = ["apple", "banana", "cherry"]

for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

print("-" * 30)

# 7. Function with Default Argument
def greet(name="Guest"):
    print(f"Hello, {name}!")

greet("Sam")
greet()

print("-" * 30)
