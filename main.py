import psutil
import os
import json
from lxml import etree as ET
import zipfile
from tkinter import Tk, filedialog  


#  Класс для 3го и 4го задания
class Person():
    def __init__(self, name=None, surname = None) -> None:
        self.name  = input('Введите имя: ') if name is None else name
        self.surname = input('Введите фамилию: ')if surname is None else surname

    def printer(self) -> None:
        print(f'Имя: {self.name}\nФамилия: {self.surname}')

    def to_xml(self):
            person_element = ET.Element("Person")
            name_element = ET.Element("Name")
            surname_element = ET.Element("Surname")

            name_element.text = self.name
            surname_element.text = str(self.surname)

            person_element.append(name_element)
            person_element.append(surname_element)

            return person_element

def create_file(end):
    filename = input(f'Введите название файла(с расширением {end}): ')

    while filename in os.listdir() or '\\' in filename or '/' in filename or not filename.endswith(f'{end}'):
          filename = input('Название файла неккоректно, введите другое: ')
    return filename

def delete_file(filename):
    if input(f'Удалить файл {filename}?(y/n): ') == 'y':
          os.remove(filename)

# Первое задание
def first_tsk(partition):
        def convert_bytes(bytes):
            # Функция для преобразования байтов в человеко-читаемый формат
            gigabytes = bytes / (1024 ** 3)
            return "{:.2f} GB".format(gigabytes)
        print('\n')
        print("Устройство:", partition.device)
        print("Точка монтирования:", partition.mountpoint)
        print("Тип файловой системы:", partition.fstype)
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            print("Размер доступного пространства:", convert_bytes(partition_usage.free))
            print("Общий размер диска:", convert_bytes(partition_usage.total))
        except PermissionError:
            # Если у вас нет разрешения для доступа к диску, выведется сообщение об ошибке.
            print("Нет разрешения для доступа к диску.")


# Второе задание
def second_tsk():
    filename = create_file('.txt')

    user_string = input('Введите строку: ')

    while len(user_string) > 200:
          user_string = input('Строка слишком длинная, введите заново: ')

    while len(user_string) == 0:
          user_string = input('Строка пустая, введите заново: ')

    with open(f'{filename}', 'w') as f:
         f.write(user_string)

    print('Строка из файла: ')

    with open(f'{filename}', 'r') as f:
         print(f.read())

    delete_file(filename)

# Третье Задание
def third_tsk():
    filename = create_file('.json')

    obj1 = Person()

    with open(filename, 'w') as f:
        f.write(json.dumps(obj1.__dict__))

    with open(filename, 'r') as f:
        json_data = f.read()

    print(f'Сериализованный объект: {json_data}')
    loaded_data = json.loads(json_data)
    loaded_person = Person(**loaded_data)

    print("\nДесериализованный объект: ")

    loaded_person.printer()

    delete_file(filename)


# Четвертое задание
def fourth_tsk():
    filename = create_file('.xml')

    obj1 = Person()

    person_element = obj1.to_xml()

    tree = ET.ElementTree(person_element)
    
    tree.write(filename, pretty_print=True, xml_declaration=True)

    print('В XML записано')
    with open(filename, 'r') as f:
        print(f.read())

    delete_file(filename)


# Пятое задание
def fifth_tsk():
    # Открываем диалоговое окно для выбора файла
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Выберите файл для архивации", filetypes=[("Все файлы", "*.*")])

    while not file_path:
        print("Файл не выбран")
        file_path = filedialog.askopenfilename(title="Выберите файл для архивации", filetypes=[("Все файлы", "*.*")])

    # Запрашиваем имя архива
    archive_name = create_file('.zip')

    try:
        # Создаем ZIP-архив и добавляем выбранный файл в архив
        with zipfile.ZipFile(archive_name, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.write(file_path, arcname=file_path.split("/")[-1])
        
        print(f"Файл '{file_path}' успешно архивирован в '{archive_name}'.")
    except Exception as e:
        print(f"Произошла ошибка при архивации файла: {e}")

  
    with zipfile.ZipFile(archive_name, 'r') as zip_ref:
        zip_ref.extractall()

    print(f"Файл '{zip_ref.namelist()[0]}' успешно разархивирован из '{archive_name}'.")

    print('Метаданные о файле: ', os.stat(zip_ref.namelist()[0]))

    delete_file(archive_name)
    delete_file(zip_ref.namelist()[0])

def main():

    menu_int = None

    while menu_int != 0:
        print('Меню\nВведите цифру для выбора задания\n 1 Информация о дисках\n 2 Работа с файлами\n 3 Работа с JSON \n 4 Работа с XML \n 5 Работа с ZIP\n 0 Выход')
        menu_int = input('Выберите задание: ')
        match menu_int:
            case '0': 
                print('Выход из программы')
            case '1':
                print('Задание 1.')
                partitions = psutil.disk_partitions()
                for partition in partitions:
                    first_tsk(partition)
                
            case '2':
                print('Задание 2.')
                second_tsk()

            case '3':
                print('Задание 3')
                third_tsk()

            case '4':
                print('Задание 4')
                fourth_tsk()
            
            case '5':
                print('Задание 5')
                fifth_tsk()
            case _:
                print('Неверное значение')


if __name__ == "__main__":
    main()
