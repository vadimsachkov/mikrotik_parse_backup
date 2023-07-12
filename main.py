import re
import os
from tkinter import filedialog as fd

def parse_backup_file(filepath):
    result = {}

    with open(filepath, 'r') as file:
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


def write_dict_to_files(data_dict, filename, size):
    file_number = 1
    # Получаем базовое имя файла и расширение
    file_name, file_ext = os.path.splitext(filename)
    # Создаем новое имя файла с добавленной переменной var
    current_file = f"{file_name}__{file_number}{file_ext}"
    file=open(current_file, "w")
    file_size = 0

    # Записываем значения словаря в файл
    for key, value in sorted(data_dict.items()):
        line = f"{value}"

        # Проверяем, не превышен ли размер файла
        if size<=0 or file_size + len(line) <= size:
            file.write(line)
            file_size += len(line)
        else:
            # Если размер превышен, закрываем текущий файл
            # и открываем следующий с новым номером
            file.close()
            file_number += 1
            current_file = f"{file_name}__{file_number}{file_ext}"
            file=open(current_file, "w")
            file.write(line)
            file_size = len(line)
    file.close()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    backup_filename=fd.askopenfilename(title="Выберите backup, экспортируемый из микротик")
    #backup_filename = "C:\\Users\\user\\Desktop\\Новая папка (4)\\2.rsc"
    parsed_commands = parse_backup_file(backup_filename)
    for name, command_body in parsed_commands.items():
        print(f'Command: {name}')
        #print(f'Body:\n{command_body}\n')
    write_dict_to_files(parsed_commands,backup_filename,0)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
