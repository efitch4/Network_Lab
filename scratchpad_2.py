class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        return f"{self.name} the {self.breed} says: Woof!"        

my_dog = Dog("Rex", "Labrador")
print(my_dog.bark())

print("-" * 30)

import random

random_number = random.randint(1, 100)
print("Random number between 1 and 100:", random_number)

print("-" * 30)

with open("output.txt", "w") as file:
    file.write("This was created by Python.\n")
    file.write("You're doing great!\n")

print("-" * 30)

for i in range(1, 4):
    for j in range(1, 4):
        product = i * j
        print(f"{i} x {j} = {product}")
    print("--- End of inner loop ---")

print("-" * 30)

def filter_even(numbers):
    return[num for num in numbers if num % 2 == 0]

original = [10, 15, 20, 25, 30]
evens = filter_even(original)
print("Even numbers:", evens)

print("-" * 30 )

fruits = ["apple", "banana", "cherry"]

for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

print("-" * 30)

def greet(name="Guest"):
    print(f"Hello, {name}!")

greet("Sam")
greet()

print("-" * 30)