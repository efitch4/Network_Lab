try:
    a = 20
    b = 10
    print(a/b)
except ZeroDivisionError:
    print('There is a divide by zero error')
finally:
    print('This is going to execute no matter what')

    