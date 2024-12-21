age = input("How old are you?")
favorite_car = input("What car do you like the most?")

print(f"So you are {age} years old ?, and your favorite car is {favorite_car}")

cars = {"Dodge": "Charger"}
print(cars)

cars[1] = "Ford:Mustang"
print(cars)

cars[2] = "Ford:Pinto"
print(cars)

del cars[2]
print(cars)

i = 0
for item in cars:
    i = i + 1
    print(i)
