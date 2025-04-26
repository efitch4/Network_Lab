class Animal:
    def sound(self):
        print("Some generic animnal sound")

    def move(self):
        print("The animal moves.")

class Dog(Animal):
    def sound(self):
        print("Woof woof!")

    def move(self):
        print("The dog runs.")

class Cat(Animal):
    def sound(self):
        print("Meow meow!")

class Bird(Animal):
    def sound(self):
        print("Tweet tweet!")

        def move(self):
            print("The bird flies.")
            super().move()

# Create instances
dog = Dog()
cat = Cat()
bird = Bird()

# Test the behavior of each animal 
dog.sound()
dog.move()

cat.sound()
cat.move()

bird.sound()
bird.move()