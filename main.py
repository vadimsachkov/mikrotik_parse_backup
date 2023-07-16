import re
import os
from tkinter import filedialog as fd
import collections
import tkinter as tk
from tkinter import simpledialog

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
# записывет каждый скрипт в отдельный именованный файл
def write_dict_to_files_byfunction(data_dict, file_path,fileprefix):
    try:
        file_number = 1

        # Разделение пути файла
        directory = os.path.dirname(file_path)
        # Разделение имени файла и расширения
        basename = os.path.basename(file_path)
        file_name, file_ext = os.path.splitext(basename)
        # Записываем значения словаря в файл
        for key, value in data_dict.items():
            line = f"{value}"
            current_file = f"{directory}/{fileprefix}_{file_number}__{key}{file_ext}"
            file = open(current_file, "w")
            file.write(line)
            file.close()
            file_number += 1
    except IOError as e:
        print(f"Ошибка при открытии или записи файла: {e}")

# фильтрует словарь команд (ключ это порядковый номер, а занчение тело команды)
# если isneed == True, то в словаре ОСТАЮТСЯ только команды, которые сооветствуют хоть одному шаблону из списка list_reg
# если isneed == False, то в словаре УДАЛЯЮТСЯ  команды, которые сооветствуют хоть одному шаблону из списка list_reg
def filter_match_dict_keys(dict_data, list_reg, isneed):

    filtered_dict = {}
    for key,value in dict_data.items():
        isfound=any(re.match(pattern, value) for pattern in list_reg)
        if (bool(isneed) == bool(isfound)) :
            filtered_dict[key] = dict_data[key]
    return filtered_dict

# фильтрует словарь команд (ключ это порядковый номер, а занчение тело команды)
# если isneed == True, то в словаре ОСТАЮТСЯ только команды, в которых найден хоть один шаблон из списка list_reg
# если isneed == False, то в словаре УДАЛЯЮТСЯ  команды, в которых найден хоть один шаблон из списка list_reg
def filter_search_dict_keys(dict_data, list_reg, isneed):

    filtered_dict = {}
    for key,value in dict_data.items():
        isfound=any(re.search(pattern, value) for pattern in list_reg)
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

# удаляет из словаря ключи, которые соот-ет хоть одному регул. шаблону из списка keylist
def remove_keys_matching_patterns(dictionary, keylist):
    pattern = '|'.join(keylist)
    keys_to_remove = [key for key in dictionary.keys() if re.search(pattern, key)]
    _ = [dictionary.pop(key) for key in keys_to_remove]

# оставляем в словаре все ключи,  которые соот-ет хоть одному регул. шаблону из списка keylist
def filter_dict_by_regex(dictionary, keylist):
    return {key: value for key, value in dictionary.items() if any(re.search(regex, key) for regex in keylist)}

if __name__ == '__main__':
    backup_filename=fd.askopenfilename(title="Выберите backup, экспортируемый из микротик")
    if backup_filename=="": exit(0)
    #backup_filename = "C:\\Users\\user\\Desktop\\Новая папка (4)\\2.rsc"
    # отпарсировать экспортирвоанные команды микротик в словарь (ключ=порядковый номер, значение=сама многострочная команда)
    commands = backup_to_dict(backup_filename)
    # фильтруем команды в словаре и оставляем только добавление cкриптов
    commands = filter_match_dict_keys(commands, [r"^/system script add"], True)
    # временно фильттрую функции GlobalFunction . так как они одинаковые
    # commands = filter_match_dict_keys(commands, [r"^[^\n]+? name=Global"], False)
    # преобразауем ключи с порядкоового номера в имена срикптов
    named_dict=key_id_to_name(commands)
    # удаляем(или оставляем ) скрипты, которые в списке
    listscripts=["GlobalFunctions.*","EnableModem"]
    #named_dict = {key: named_dict[key] for key in named_dict if key not in listscripts}
    remove_keys_matching_patterns(named_dict, listscripts)
    # выводим список ключей , который будут записаны в файлы
    for name, command_body in named_dict.items():
        print(f'Command: {name}')
        #print(f'Body:\n{command_body}')
    # записывапем словарь в файлы, ограничивая размер (третий параметр)
    write_dict_to_files(named_dict, backup_filename, 0)
    # записывет каждый скрипт в отдельный именованный файл
    # Создание главного окна
    root = tk.Tk()
    # Скрытие главного окна
    root.withdraw()
    # Запрос ввода строки у пользователя в диалоговом окне
    user_input_fileprefix = simpledialog.askstring("Введите префикс файлов:", "Введите префикс файлов для скриптов, например m61")
    #user_input_fileprefix = input("Введите префикс файлов для скриптов, например m61: ")
    write_dict_to_files_byfunction(named_dict, backup_filename,user_input_fileprefix)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
