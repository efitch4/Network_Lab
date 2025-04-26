# Basic Syntax and Variables
def basic_syntax_demo():
    name = "Alice"
    age = 30
    height = 5.7
    is_programmer = True
    
    print(f"Name: {name}")
    print(f"Age: {age}")
    print(f"Height: {height}")
    print(f"Is Programmer: {is_programmer}\n")

# Functions and Conditionals
def check_even_odd(number):
    if number % 2 == 0:
        return f"{number} is even"
    else:
        return f"{number} is odd"

def temperature_converter(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return f"{celsius}°C is equal to {fahrenheit}°F"

# Loops and Lists
def list_demo():
    fruits = ["apple", "banana", "cherry", "date"]
    print("Fruits list:")
    for fruit in fruits:
        print(fruit)
    
    print("\nEnumerated list:")
    for index, fruit in enumerate(fruits):
        print(f"{index}: {fruit}\n")

# Dictionaries and Sets
def dictionary_set_demo():
    student_grades = {
        "Alice": 90,
        "Bob": 85,
        "Charlie": 95
    }
    print("Student Grades:")
    for student, grade in student_grades.items():
        print(f"{student}: {grade}")
    
    unique_numbers = {1, 2, 3, 3, 4, 5}
    print(f"\nUnique Numbers: {unique_numbers}\n")

# File Handling and Error Handling
def file_handling_demo(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            print(f"Content of {filename}:\n{content}\n")
    except FileNotFoundError:
        print(f"Error: {filename} not found.\n")

# Classes and Object-Oriented Programming
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def make_sound(self):
        print(f"{self.name} the {self.species} says: Hello!")

class Dog(Animal):
    def make_sound(self):
        print(f"{self.name} the {self.species} barks: Woof!")

class Cat(Animal):
    def make_sound(self):
        print(f"{self.name} the {self.species} meows: Meow!")

# Modules and Importing
import math

def math_module_demo():
    num = 16
    sqrt = math.sqrt(num)
    print(f"Square root of {num} is {sqrt}\n")

# Lambda Functions and List Comprehensions
def lambda_list_comprehension_demo():
    numbers = [1, 2, 3, 4, 5]
    squares = list(map(lambda x: x**2, numbers))
    print(f"Squares: {squares}")
    
    even_numbers = [x for x in numbers if x % 2 == 0]
    print(f"Even Numbers: {even_numbers}\n")

# Recursion Example
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)

# Main function to call all the demos
def main():
    basic_syntax_demo()
    print(check_even_odd(5))
    print(check_even_odd(10))
    print(temperature_converter(25))
    
    list_demo()
    dictionary_set_demo()
    
    file_handling_demo("sample.txt")
    
    dog = Dog("Buddy", "Dog")
    cat = Cat("Whiskers", "Cat")
    dog.make_sound()
    cat.make_sound()
    
    math_module_demo()
    lambda_list_comprehension_demo()
    
    print(f"Factorial of 5: {factorial(5)}")

if __name__ == "__main__":
    main()
