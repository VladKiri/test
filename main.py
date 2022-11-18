import csv
import re
import textwrap
from prettytable import PrettyTable
import os

dic_naming = {'№': '№', 'name': 'Название', 'description': 'Описание', 'key_skills': 'Навыки',
              'experience_id': 'Опыт работы',
              'premium': 'Премиум-вакансия', 'employer_name': 'Компания', 'salary_from': 'Оклад               ',
              'area_name': 'Название региона', 'published_at': 'Дата публикации вакансии'}

dic_yer = {"noExperience": "Нет опыта", "between1And3": "От 1 года до 3 лет",
           "between3And6": "От 3 до 6 лет", "moreThan6": "Более 6 лет"}

dic_val = {"AZN": "Манаты", "BYR": "Белорусские рубли", "EUR": "Евро", "GEL": "Грузинский лари",
           "KGS": "Киргизский сом", "KZT": "Тенге", "RUR": "Рубли", "UAH": "Гривны", "USD": "Доллары",
           "UZS": "Узбекский сум"}


def money_editor(x):
    string = str(x)
    if '.' in string: string = string[:-2]
    new_string = ''
    for i in range(len(string)):
        new_string = string[-3:] + ' ' + new_string
        string = string[:-3]
    return new_string.strip()


def csv_reader(file_name):
    with open(file_name, encoding='utf-8-sig') as file:
        readers = csv.reader(file)
        reader = readers.__next__()
        list_naming = [row for row in readers]
        return reader, list_naming


def csv_filer(reader, list_naming):
    data_vacancies = []
    for row in list_naming:
        dictionary = {}
        if (len(row) != len(reader)) or ('' in row): continue
        for key, value in zip(reader, row):
            if '\n' in value:
                div = [' '.join(re.sub(r"<[^>]+>", '', el).split()) for el in value.split('\n')]
                dictionary[key] = ','.join(div)
            else:
                dictionary[key] = ' '.join(re.sub(r"<[^>]+>", '', value).split())
        data_vacancies.append(dictionary)
    return data_vacancies


def formatter(row):
    dictionary = row
    if dictionary['premium'] == "False":
        dictionary['premium'] = "Нет"
    else:
        dictionary['premium'] = "Да"
    if dictionary['salary_gross'] == "False":
        dictionary['salary_gross'] = "Нет"
    else:
        dictionary['salary_gross'] = "Да"
    if dictionary['salary_gross'] == 'Да':
        tax = 'Без вычета налогов'
    else:
        tax = 'С вычетом налогов'
    dictionary['salary_from'] = f"{money_editor(dictionary['salary_from'])} - {money_editor(dictionary['salary_to'])} " \
                                f"({dic_val[dictionary['salary_currency']]}) ({tax})"
    dictionary['experience_id'] = dic_yer[dictionary['experience_id']]
    dictionary['published_at'] = f"{dictionary['published_at'][8:10]}.{dictionary['published_at'][5:7]}." \
                                 f"{dictionary['published_at'][:4]}"
    del dictionary['salary_to'], dictionary['salary_currency'], dictionary['salary_gross']
    return dictionary


def tabl_form(x, i):
    divs = [str(i + 1)]
    for key, value in x.items():
        if key == 'key_skills':
            if len(value) > 100:
                el = value[:100] + '...'
            else:
                el = value
            string = ''
            for k in el.split(','):
                string += textwrap.fill(k, width=20)
                string += '\n'
            divs.append(string[:-1])
        else:
            if len(value) > 100:
                el = value[:100] + '...'
            else:
                el = value
            divs.append(textwrap.fill(el, width=20))
    return divs


def print_vacancies(data_vacancies, dic_naming):
    table = PrettyTable()
    table.field_names = dic_naming.values()
    for i in range(len(data_vacancies)):
        row = formatter(data_vacancies[i])
        table.add_row(tabl_form(dict(row), i))
    table.align = "l"
    table.hrules = True
    print(table)


file = input()
if os.stat(file).st_size == 0:
    print('Пустой файл')
else:
    reader, list_naming = csv_reader(file)
    data_vacancies = csv_filer(reader, list_naming)
    if len(data_vacancies) == 0:
        print('Нет данных')
    else:
        print_vacancies(data_vacancies, dic_naming)
