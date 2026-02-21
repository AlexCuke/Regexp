from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
#pprint(contacts_list)


# Функция для форматирования телефона
def format_phone(phone):
    # Удаляем все символы кроме цифр
    cleaned = re.sub(r'\D', '', phone)
    
    # Проверяем наличие добавочного номера
    if 'доб' in phone.lower():
        # Ищем есть ли добавочный номер.Выделяем
        match = re.search(r'(\d{11})\D*(доб\.\s*(\d+))?', phone, re.IGNORECASE)
        if match:
            main_number = match.group(1)
            ext = match.group(2) if match.group(2) else ''
            formatted = f"+7({main_number[1:4]}){main_number[4:7]}-{main_number[7:9]}-{main_number[9:]}"
            if ext:
                return f"{formatted} доб.{ext.split('.')[1].strip()}"
            return formatted
    
    # Форматируем обычный номер
    if len(cleaned) == 11:
        return f"+7({cleaned[1:4]}){cleaned[4:7]}-{cleaned[7:9]}-{cleaned[9:]}"
    return phone
  
# TODO 1: выполните пункты 1-3 ДЗ
# Обработка контактов
contacts_in_work = []

for contact in contacts_list[1:]:  # со второй строки
    # Разбиваем ФИО
    full_name = ' '.join(contact[:2]).split()
    
    if len(full_name) == 3:
        lastname, firstname, surname = full_name
    elif len(full_name) == 2:
        lastname, firstname = full_name
        surname = ''
    else:
        lastname = full_name[0] if full_name else ''
        firstname = ''
        surname = ''
    
    # Форматируем номер телефона
    formatted_phone = format_phone(contact[5])
    
    # Собираем  контакт
    contacts_in_work.append([
        lastname,
        firstname,
        surname,
        contact[3] or '',
        contact[4] or '',
        formatted_phone,
        contact[6] or ''
    ])


# Создаем словарь для группировки контактов
contacts_dict = {}
for contact in contacts_in_work:
    key = (contact[0], contact[1])  # Ключ по Фамилии и имени ()
    
    if key not in contacts_dict:
        contacts_dict[key] = {
            'lastname': contact[0],
            'firstname': contact[1],
            'surname': contact[2],
            'organizations': set(),
            'positions': set(),
            'phones': set(),
            'emails': set()
        }
    
    # Добавляем уникальные значения
    contacts_dict[key]['organizations'].add(contact[3])
    contacts_dict[key]['positions'].add(contact[4])
    contacts_dict[key]['phones'].add(contact[5])
    contacts_dict[key]['emails'].add(contact[6])
pprint(contacts_dict)
# Формируем финальный список контактов
final_contacts = []

for key, data in contacts_dict.items():
    final_contacts.append([
        data['lastname'],
        data['firstname'],
        data['surname'],
        ', '.join(data['organizations']),
        ', '.join(data['positions']),
        ', '.join(data['phones']),
        ', '.join(data['emails'])
    ])
# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerow(["lastname","firstname","surname","organization","position","phone","email"])
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(final_contacts)