import datetime

with open('show_commands.txt') as show_cmd:
    commands = show_cmd.readlines()
# time_seq_no_commands
#print(commands)
now = datetime.datetime.now().replace(microsecond=0)
for cmd in enumerate(commands, start=1):
    file_name = f"{str(now).replace(' ', '_').replace(':', '_')}){str(cmd[0]).zfill(2)}_{cmd[1].replace(' ', '_').strip()}.txt"

    # file_name = f"{str(now).replace(' ', ':')}){str(cmd[0]).zfill(2)}_{cmd[1].replace(' ', '_').strip()}.txt"
    with open(file_name, 'w') as cmd_data:
        cmd_data.write('test_data')
