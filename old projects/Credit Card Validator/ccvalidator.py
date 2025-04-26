card_no = "5178058017314405"
odd_sum = 0
even_sum = 0
double_list = []
number = list (card_no)
for (idx,val) in enumerate(number):
    if idx %2 !=0: # this is an odd number
        odd_sum += int(val)
    else:               # this is an even number
        double_list.append(int(val)*2)

#converting the list into a string
double_string = ""
for x in double_list:
    double_string += str(x)

#converting the string back to a list
double_list = list(double_string)

for x in double_list:
    even_sum += int(x)

net_sum = odd_sum + even_sum
if net_sum %10 ==0:
    print('Valid card!')
else:
    print('Invalid card')

# Sum of odd index number
# Double the value of even numbers *2
# For even if the sum the number is a 2 digit number you will need to add both up 
# For example 1 + 0 = 1


# 5 6 1 0 5 9 1 0 8 1   0   1   8   2   5    0
# 1 2 3 4 5 6 7 8 9 1-0 11  12  13  14  15  16

#    