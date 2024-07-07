import requests
import bs4
from fake_headers import Headers
import json
from tqdm import tqdm
import re

def get_headers():
    return Headers(os='win', browser='chrome').generate()

for page in tqdm(range(0, 5), desc='Поиск по страницам сайта '):
    response = requests.get(f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={page}', headers=get_headers())

    main_html_data = response.text
    main_soup = bs4.BeautifulSoup(main_html_data, features='lxml')
    tag_vacancy_list = main_soup.find('main', class_='vacancy-serp-content')
    vacancy_tags = tag_vacancy_list.find_all('div', class_='serp-item_link')

    parsed_data = []

    for vacancy_tag in vacancy_tags:
        h2_tag = vacancy_tag.find('h2', class_='bloko-header-section-2')
        title = h2_tag.text
        a_tag = h2_tag.find('a')
        vacancy_link = a_tag['href']

        if 'Django' in title or 'flask' in title:
            vacancy_link_response = requests.get(vacancy_link, headers=get_headers())
            vacancy_html_data = vacancy_link_response.text

            vacancy_soup = bs4.BeautifulSoup(vacancy_html_data, features='lxml')
            company_tag = vacancy_soup.find('div', class_='vacancy-company-details')
            c_name = company_tag.find('span').text.replace(' ', ' ')
            salary = vacancy_soup.find('span', class_='magritte-text___pbpft_3-0-9').text.replace(' ', ' ')
            company_adress = vacancy_soup.find('a', class_='magritte-link___b4rEM_4-1-4').text

            parsed_data.append({
                'Название вакансии': title,
                'Ссылка': vacancy_link,
                'Название компании': c_name,
                'Зарплата': salary,
                'Адрес': company_adress
            })

        else:
            continue

        filename = 'data.json'
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(parsed_data, file, indent=4, ensure_ascii=False)

print(f'Количество вакансий равно: {len(parsed_data)}')

