# !/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
import sys
from task_2_packet import *

# Использовать словарь, содержащий следующие ключи: фамилия, имя; номер телефона;
# дата рождения (список из трех чисел). Написать программу, выполняющую следующие
# действия: ввод с клавиатуры данных в список, состоящий из словарей заданной структуры;
# записи должны быть размещены по алфавиту; вывод на экран информации о людях, чьи
# дни рождения приходятся на месяц, значение которого введено с клавиатуры; если таких
# нет, выдать на дисплей соответствующее сообщение.

# Выполнить индивидуальное задание 2 лабораторной работы 13, добавив возможность работы с
# исключениями и логгирование.


if __name__ == '__main__':
    staff = Staff.Staff()
    logging.basicConfig(
        filename='workers.log',
        level=logging.INFO
    )

    while True:
        try:
            command = input("Enter command> ").lower()

            if command == "exit":
                break

            elif command == "add":
                las_name = str(input("Enter last name>  "))
                name = str(input("Enter first name> "))
                tel = str(input("Enter phone> +"))
                date = list(map(int, input("Enter birthdate separated by space> ").split(" ")))
                staff.add(las_name, name, tel, date)
                logging.info(
                    f"Добавлен сотрудник: {las_name}, {name}"
                    f"Номер телефона +{tel}"
                    f"Дата рождения {date[0]}.{date[1]}.{date[2]}"
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
                raise UnknownCommandError.UnknownCommandError(command)
        except Exception as exc:
            logging.error(f"Ошибка: {exc}")
            print(exc, file=sys.stderr)
