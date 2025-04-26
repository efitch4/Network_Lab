# Abstract class
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def sound(self):
        pass

    def description(self):
        return "This is an animal."

# Encapsulation
class Dog(Animal):
    def __init__(self, name, breed):
        self.__name = name  # Private attribute
        self.__breed = breed  # Private attribute

    def sound(self):
        return "Woof!"

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_breed(self):
        return self.__breed

    def set_breed(self, breed):
        self.__breed = breed

# Inheritance
class Cat(Animal):
    def __init__(self, name):
        self.__name = name

    def sound(self):
        return "Meow!"

    def get_name(self):
        return self.__name

# Polymorphism
def animal_sound(animal: Animal):
    return animal.sound()

# Example usage
if __name__ == "__main__":
    # Creating objects
    dog = Dog("Buddy", "Golden Retriever")
    cat = Cat("Whiskers")

    # Using encapsulation
    print(f"Dog's name: {dog.get_name()}, Breed: {dog.get_breed()}")
    print(f"Cat's name: {cat.get_name()}")

    # Using polymorphism
    print(f"Dog sounds: {animal_sound(dog)}")
    print(f"Cat sounds: {animal_sound(cat)}")

    # Demonstrating abstraction
    print(dog.description())
    print(cat.description())
