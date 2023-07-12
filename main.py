import re

def parse_backup_file(filename):
    result = {}

    with open(filename, 'r') as file:
        command_name = ''
        command_body = ''

        for line in file:
            #line = line.strip()

            if line.startswith('/system script add'):
                if command_name != '':
                    result[command_name] = command_body

                command_name = line.split('name=')[1].split()[0]
                command_body = line

            elif line.startswith(' '):
                command_body += line

    if command_name != '':
        result[command_name] = command_body

    return result

def write_dict_to_file(dictionary, filename):
    with open(filename, 'w') as file:
        for value in dictionary.values():
            file.write(str(value) )

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    backup_filename = "C:\\Users\\user\\Desktop\\2.rsc"
    parsed_commands = parse_backup_file(backup_filename)
    for name, command_body in parsed_commands.items():
        print(f'Command: {name}')
        #print(f'Body:\n{command_body}\n')
    write_dict_to_file(parsed_commands,"C:\\Users\\user\\Desktop\\2_.rsc")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
