from pprint import pprint
import csv
import re

"""Читаем адресную книгу в формате CSV в список contacts_list:"""
with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

"""Приводим шаблон ФИО к нужному формату:"""
phones_book = []
full_name_template = r'(^[А-Я]\w+) ?,?(\w+) ?,?(\w+)?'
change_full_name_template = r'\1,\2,\3'

for i in contacts_list:
    while '' in i:
        i.remove('')
    result = re.sub(full_name_template, change_full_name_template, ','.join(i))
    phones_book.append(result)

"""Приводим шаблон телефонного номера к нужному формату:"""
phone_number_template = r'(\+7|8) ?\(?(\d{3})\)?-? ?(\d{3})\-? ?(\d{2})-? ?(\d{2}) ?\(?(доб\.)? ?(\d+)?(\))?'
change_phone_number_template = r'+7(\2)\3-\4-\5 \6\7'
for i, j in enumerate(phones_book):
    j = j.split(',')
    result = re.sub(phone_number_template, change_phone_number_template, ','.join(j))
    phones_book[i] = result

phones_book_dict = {}
for _ in phones_book:
    if list(phones_book_dict.keys()).count(','.join(_.split(',')[0:2])):
        phones_book_dict[','.join(_.split(',')[0:2])] += f",{','.join(_.split(',')[2:])}"
    else:
        phones_book_dict.setdefault(','.join(_.split(',')[0:2]), ','.join(_.split(',')[2:]))

phones_book_sort = []
for i, j in phones_book_dict.items():
    phones_book_sort.append(list(i.split(',')) + list(j.split(',')))

phones_book_final = []
for i in phones_book_sort:
    i = list(dict().fromkeys(i))
    for j in i:
        if j[0] == '+':
            if j.count('доб'):
                i.append(i.pop(i.index(j)))
            else:
                if j.count(' '):
                    i.append(i.pop(i.index(j)).replace(' ', ''))
    for k in i:
        if k.count('@'):
            i.append(i.pop(i.index(k)))
    phones_book_final.append(i)

with open("phonebook.csv", "w", encoding="utf8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(phones_book_final)
