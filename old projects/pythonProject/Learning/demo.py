file = open("demo.txt", 'w')
file.write("This is the text written to the file")
file.close()

file = open("demo.txt", 'r')
content = file.read()
print(content)
file.close()

file = open("demo.txt", 'w')
file.write("This is the new line")
file.close
