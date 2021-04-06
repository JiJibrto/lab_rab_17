# !/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import sys
import task_1_mod as tm

# Использовать словарь, содержащий следующие ключи: фамилия, имя; номер телефона;
# дата рождения (список из трех чисел). Написать программу, выполняющую следующие
# действия: ввод с клавиатуры данных в список, состоящий из словарей заданной структуры;
# записи должны быть размещены по алфавиту; вывод на экран информации о людях, чьи
# дни рождения приходятся на месяц, значение которого введено с клавиатуры; если таких
# нет, выдать на дисплей соответствующее сообщение.

# Выполнить индивидуальное задание 2 лабораторной работы 13, добавив возможность работы с
# исключениями и логгирование.

# Изучить возможности модуля logging. Добавить для предыдущего задания вывод в файлы лога
# даты и времени выполнения пользовательской команды с точностью до миллисекунды.


if __name__ == '__main__':
    staff = tm.Staff()
    logging.basicConfig(
        filename='workers.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s:%(message)s'
    )
    logging.info("Программа начала работу")
    while True:
        try:
            command = input("Enter command> ").lower()

            if command == "exit":
                logging.info("Программа завершила работу")
                break

            elif command == "add":
                las_name = str(input("Enter last name>  "))
                name = str(input("Enter first name> "))
                tel = str(input("Enter phone> +"))
                date = list(map(int, input("Enter birthdate separated by space> ").split(" ")))
                staff.add(las_name, name, tel, date)
                logging.info(
                    f"\nДобавлен сотрудник: {las_name}, {name}"
                    f"\nНомер телефона +{tel}"
                    f"\nДата рождения {date[0]}.{date[1]}.{date[2]}"
                )

            elif command == "list":
                print(staff)
                logging.info("Отображен список сотрудников.")

            elif command.startswith('load '):
                # Разбить команду на части для выделения имени файла.
                parts = command.split(' ', maxsplit=1)
                staff.load(parts[1])
                logging.info(f"Загружены данные из файла {parts[1]}.")

            elif command.startswith('save '):
                # Разбить команду на части для выделения имени файла.
                parts = command.split(' ', maxsplit=1)
                staff.save(parts[1])
                logging.info(f"Сохраннены данные в файла {parts[1]}.")

            elif command == 'help':
                # Вывести справку о работе с программой.
                print("Список команд:\n")
                print("add - добавить работника;")
                print("list - вывести список работников;")
                print("task - вывести сотрудников определенной даты рождения")
                print("load <имя файла> - загрузить данные из файла;")
                print("save <имя файла> - сохранить данные в файл;")
                print("exit - выход из программы;")
            else:
                raise tm.UnknownCommandError(command)
        except Exception as exc:
            logging.info("Программа завершила работу")
            logging.error(f"Ошибка: {exc}")
            print(exc, file=sys.stderr)