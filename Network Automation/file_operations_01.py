import os
#
# # Seth the path to the Paramiko log file
# print(os.getcwd())
# os.chdir('C:/Users/Eric/OneDrive/Desktop/pypro/Network Automation')
# print(os.getcwd())
# print(len(os.listdir()))
# print(f"Current working directory is {os.getcwd()}")
# print(os.system('ls -larth'))
#
# files = (os.listdir())
# files.sort()
#
# for file in files:
#     #   print(file)
# #     with open(file) as file_data:
# #         if "paramiko" in file.casefold():
# #             print(print(f"\n\n{'#' * 10}{file}{'#' * 10}"))
# #             # print(type(file_data))
# #             # print(dir(file_data))
# #             print(file_data.read())
# file1.close()
# file1 = open('config1.txt', 'r')
# #print(dir(file1))
# #(file1.read())
# commands = (file1.readlines())
# for command in commands:
#     print(command.rstrip('\n'))
# ''' with open '''
# with open('config1.txt') as file1:
#     commands = file1.readlines()
#
# for command in commands:
#     print(command.rstrip('\n'))
#
# with open('config2.txt', 'w') as file2:
#     file2.write("testdata3\ntestdata4\n")
#
# with open('test.pdf', 'rb') as source_file:
#     s = source_file.read()
# with open('new_file.pdf', 'wb') as dest_file:
#     dest_file.write(s)

os.remove('new_file.pdf')