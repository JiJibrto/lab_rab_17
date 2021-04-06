from dataclasses import dataclass, field
from typing import List
import xml.etree.ElementTree as ET


class UnknownCommandError(Exception):
    def __init__(self, command, message="Unknown command"):
        self.command = command
        self.message = message
        super(UnknownCommandError, self).__init__(message)

    def __str__(self):
        return f"{self.command} -> {self.message}"


@dataclass(frozen=True)
class Worker:
    las_name: str
    name: str
    tel: int
    date: list


@dataclass
class Staff:
    workers: List[Worker] = field(default_factory=lambda: [])

    def add(self, las_name, name, tel, date):
        self.workers.append(
        Worker(
            las_name=las_name,
            name=name,
            tel=tel,
            date=date
        )
        )
        self.workers.sort(key=lambda worker: worker.name)

    def __str__(self):
        # Заголовок таблицы.
        table = []
        line = "+-{}-+-{}-+-{}-+-{}-+-{}-+".format(
            '-' * 4,
            '-' * 15,
            '-' * 15,
            '-' * 20,
            '-' * 20
        )
        table.append(line)
        table.append((
                "| {:^4} | {:^15} | {:^15} | {:^20} | {:^20} |".format(
                    "№",
                    "Фамилия",
                    "Имя",
                    "Телефон",
                    "Дата рождения"
                )
            )
        )
        table.append(line)
        # Вывести данные о всех сотрудниках.
        for idx, worker in enumerate(self.workers, 1):
            table.append(
                '| {:>4} | {:<15} | {:<15} | {:>20} | {:^20} |'.format(
                        idx,
                        worker.las_name,
                        worker.name,
                        worker.tel,
                        ".".join(map(str, worker.date))
                    )
            )
            table.append(line)
        return '\n'.join(table)

    def load(self, filename):
        with open(filename, 'r', encoding='utf8') as fin:
            xml = fin.read()
        parser = ET.XMLParser(encoding="utf8")
        tree = ET.fromstring(xml, parser=parser)
        self.workers = []
        for worker_element in tree:
            las_name, name, tel, date = None, None, None, None
        for element in worker_element:
            if element.tag == 'las_name':
                las_name = element.text
            elif element.tag == 'name':
                name = element.text
            elif element.tag == 'tel':
                tel = int(element.text)
            elif element.tag == 'date':
                date = list(map(int, element.text.split(" ")))
        if las_name is not None and name is not None \
                and tel is not None and date is not None:
            self.workers.append(
                Worker(
                    las_name=las_name,
                    name=name,
                    tel=tel,
                    date=date
                )
            )

    def save(self, filename):
        root = ET.Element('workers')
        for worker in self.workers:
            worker_element = ET.Element('worker')

            las_name_element = ET.SubElement(worker_element, 'las_name')
            las_name_element.text = worker.las_name

            name_element = ET.SubElement(worker_element, 'name')
            name_element.text = worker.name

            tel_element = ET.SubElement(worker_element, 'tel')
            tel_element.text = worker.tel

            date_element = ET.SubElement(worker_element, 'date')
            date_element.text = ' '.join(map(str, worker.date))

            root.append(worker_element)

        tree = ET.ElementTree(root)
        with open(filename, 'wb') as fout:
            tree.write(fout, encoding='utf8', xml_declaration=True)

