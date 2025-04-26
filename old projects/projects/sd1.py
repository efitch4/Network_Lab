# length =  float(input("Enter the length"))
# width = float(input("Enter the width"))

# area = (length * width)

# print(f"The area is  {area}")


def add(a,b):
    return a + b

def square(c):
    return c * c

result = square(add(3,4))

print(result)

def main():
    student = get_student()
    print(f"{student[0]} from {student[1]}")

def get_student():
    student = {}
    student["name"] = input("Name:")
    student["house"] = input("House:")
    return student