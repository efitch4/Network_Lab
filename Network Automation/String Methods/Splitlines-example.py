# show_output = '''GigabitEthernet1       192.168.204.138 YES DHCP   up                    up
# GigabitEthernet2       unassigned      YES NVRAM  administratively down down
# GigabitEthernet3       unassigned      YES NVRAM  administratively down down
# GigabitEthernet4       unassigned      YES NVRAM  administratively down down
# Loopback1001           1.1.1.1         YES NVRAM  up                    up
# '''
#
# intf_lines = show_output.splitlines()
# # print(intf_lines)
# for intf in intf_lines:
#     intf_details = intf.split()
#     if intf_details[1] == "unassigned":
#         continue
#     print(f"Interface name : {intf_details[0]} Interface IP {intf_details[1]}")
#
######################################################################################

with open('output.txt') as text:
    lines = text.readlines()
# print(lines)
    print("Press Enter...", end='')
    for line in lines:
        if input() == '':
            line = line.strip('\n')
            print(line, end='')
    print("Completed")
