import re
import os
from tkinter import filedialog as fd
import collections


# парсирует файл экспортированный  из микротик командой export terse file=$fn;
# и записывает в словарь команды по порядку. (ключ=порядковый номер, значение=сама многострочная команда)
def backup_to_dict(filepath):
    result = {}

    with open(filepath, 'r') as file:
        command_name = ''
        command_body = ''
        command_id=0

        for line in file:
            #line = line.strip()
            if (line) == '\n': continue
            if not line.startswith(' '):
                command_id += 1
                if command_id >1:
                    result[command_id] = command_body
                command_body = line
            else:
                command_body += line

    if command_id >1:
        result[command_id] = command_body

    return result

# записывает словарь в файлы с именем  filename (добавляя к имени файла __ и порядковый номер)
def write_dict_to_files(data_dict, filename, size):
    try:
        file_number = 1
        # Получаем базовое имя файла и расширение
        file_name, file_ext = os.path.splitext(filename)
        # Создаем новое имя файла с добавленной переменной var
        current_file = f"{file_name}__{file_number}{file_ext}"
        file=open(current_file, "w")
        file_size = 0

        # Записываем значения словаря в файл
        #for key, value in sorted(data_dict.items()):
        for key, value in data_dict.items():
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
    except IOError as e:
        print(f"Ошибка при открытии или записи файла: {e}")

# фильтрует словарь команд (ключ это порядковый номер, а занчение тело команды)
# если isneed == True, то в словаре ОСТАЮТСЯ только команды, которые сооветствуют хоть одному шаблону из списка list_reg
# если isneed == False, то в словаре УДАЛЯЮТСЯ  команды, которые сооветствуют хоть одному шаблону из списка list_reg
def filter_dict_keys(dict_data, list_reg, isneed):

    filtered_dict = {}
    for key,value in dict_data.items():
        isfound=any(re.match(pattern, value) for pattern in list_reg)
        if (bool(isneed) == bool(isfound)) :
            filtered_dict[key] = dict_data[key]
    return filtered_dict

# возвращает словарь гдн ключи (порядковый номер команды)заменены на имена скриптов из поля name=
# должна применяться только для команд добавления скриптов
#  Возвращаемый словрь типа collections.OrderedDict() с отсортированным списком ключей
def key_id_to_name(dict_data):
    dict={}
    # заменяем названия ключей с порядкового номера на имя скрипта, дабавляемого командой /system script add
    for key in dict_data.keys():
        line=dict_data[key]
        command_name = line.split('name=')[1].split()[0]
        if len(command_name)==0: command_name=key
        dict [command_name]=line
    sorted_dict=collections.OrderedDict()
    for key, value in sorted(dict.items()):
        sorted_dict[key]=value
    return sorted_dict


if __name__ == '__main__':
    backup_filename=fd.askopenfilename(title="Выберите backup, экспортируемый из микротик")
    #backup_filename = "C:\\Users\\user\\Desktop\\Новая папка (4)\\2.rsc"
    # отпарсировать экспортирвоанные команды микротик в словарь (ключ=порядковый номер, значение=сама многострочная команда)
    parsed_commands = backup_to_dict(backup_filename)
    # фильтруем команды в словаре и ОСТАВЛЯЕМ (3-1 параметр = true, иначе- удаляем))только добавление cкриптов
    filtered_commands=filter_dict_keys(parsed_commands, [r"^/system script add"],True)
    filtered_commands = filter_dict_keys(filtered_commands, [r"^[^\n]+? name=Global"], False)
    # преобразауем ключи с порядкоового номера в имена срикптов
    named_dict=key_id_to_name(filtered_commands)
    # выводим список ключей , которые будут записаны в файлы
    for name, command_body in named_dict.items():
        print(f'Command: {name}')
        #print(f'Body:\n{command_body}')
    # записывапем словарь в файлы.  третий параметр  - это макс размер одного файла (0=безлимит)
    write_dict_to_files(named_dict, backup_filename, 0)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
