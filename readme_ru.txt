
README — mikrotik_script_export_splitter  
Автор: Вадим Сачков  
Дата: 2025-03-28

---

1. Назначение

Данная утилита предназначена для автоматической обработки скриптов, экспортированных из MikroTik RouterOS.  
Работает исключительно с командами /system script add, содержащими тексты скриптов, и выполняет разбиение, фильтрацию и сохранение их в виде отдельных файлов.

Зачем это нужно:

В некоторых конфигурациях MikroTik (особенно при использовании скриптов) скриптов может быть много, и они могут быть большими.  
При попытке переноса такой конфигурации на другой роутер с помощью импорта .rsc-файла MikroTik может:

- обрезать файл,
- выдать ошибку,
- или частично загрузить скрипты, нарушив их структуру.

Чтобы избежать этого, скрипты необходимо заранее разбить на отдельные файлы или разделить по частям — именно это и делает утилита автоматически.

---

2. Возможности

- Извлечение всех команд /system script add из .rsc-файла
- Фильтрация скриптов по имени (оставить/исключить)
- Переименование ключей в словаре на основе name=
- Сохранение скриптов:
  - В один или несколько файлов (с ограничением по размеру)
  - Каждый скрипт — в отдельный файл
- Генерация файла с командами удаления соответствующих скриптов
- Ввод префикса для имен выходных файлов через GUI-диалог

---

3. Системные требования

- Python 3.x
- ОС Windows (используется tkinter)
- Установленные модули: tkinter, collections, re, os

---

4. Как использовать

1. Запустите main.py
2. Выберите .rsc-файл, экспортированный из MikroTik через:
       /export terse file=имя
3. Программа выполнит:
   - Поиск всех команд /system script add
   - Фильтрацию (например, исключение лишних скриптов)
   - Разделение по размеру
   - Сохранение в файлы
   - Создание файла с командами удаления
4. В диалоговом окне введите префикс для имен файлов скриптов

---

5. Настройки фильтрации

Скрипты можно исключать из обработки по имени с помощью списка listscripts.

В коде:
    listscripts = ["EnableModem", "~.+"]
    remove_keys_matching_patterns(named_dict, listscripts)

Если имя скрипта совпадает с любым шаблоном в списке — он будет удалён из словаря перед сохранением.

Примеры:
- "EnableModem" — удалит скрипт с точным именем EnableModem
- "~.+" — удалит все скрипты, чьи имена начинаются с символа ~ и содержат ещё хотя бы один символ  
  Подойдут для удаления временных или отладочных скриптов, например:
    - ~DebugScript
    - ~Temp1
    - ~test_import

Если вы хотите сохранить все скрипты, просто оставьте список пустым:
    listscripts = []

Или закомментируйте строку вызова remove_keys_matching_patterns(...).

---

6. Форматы выходных файлов

- имяфайла__1.rsc, имяфайла__2.rsc и т.д. — если общий размер превышает заданный лимит
- префикс_1__ScriptName.rsc, префикс_2__ScriptName.rsc и т.д. — каждый скрипт в отдельном файле
- имяфайла__remove.rsc — команды /system script remove <имя>

---

7. Пример запуска

- Вы экспортировали конфигурацию:
      /export terse file=scripts.rsc
- Запускаете main.py
- Выбираете scripts.rsc
- Вводите префикс m61
- Получаете файлы:
      scripts__1.rsc  
      scripts__remove.rsc  
      m61_1__MyScript.rsc  
      m61_2__AnotherScript.rsc  
      ...

---

8. Ограничения

- Работает только с командами /system script add  
- Не обрабатывает другие части конфигурации
- Только Windows (используется GUI tkinter)
- Размер ограничения задаётся в байтах (по умолчанию: 50000)

---

9. Контакты

Автор: Вадим Сачков  
[Добавьте ссылку на GitHub или контакт при публикации]
