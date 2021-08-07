""" Вариант 1
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов
Superjob и HH.
Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (отдельно минимальную и максимальную).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия. ### По желанию можно добавить ещё параметры вакансии
(например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas.
"""

from bs4 import BeautifulSoup as bs
import requests
import lxml
import re
import pandas as pd
from fake_headers import Headers


def hh(vac):
    vak_dict = []
    page_num = 0
    while page_num <= 2:
        param = {'text': vac, 'search_field': 'name', 'items_on_page': '100', 'page': page_num}

        header = Headers(headers=True).generate()
        url = 'https://hh.ru/search/vacancy/'
        response = requests.get(url, params=param, headers=header)
        soup = bs(response.text, 'lxml')
        # print(soup.prettify())

        vacancy_items = soup.find('div', {'data-qa': 'vacancy-serp__results'}).find_all('div',
                                                                                        {'class': 'vacancy-serp-item'})

        for i in vacancy_items:
            new_data = {}
            new_data['name'] = i.find(class_='resume-search-item__name').text
            new_data['company_name'] = i.find(class_='vacancy-serp-item__meta-info').text
            new_data['city'] = i.find('span', class_='vacancy-serp-item__meta-info').text
            # salary = i.find( class_='vacancy-serp-item__sidebar').text
            salary = i.find('div', {'class': 'vacancy-serp-item__sidebar'})
            if not salary:
                new_data['salary_min'] = None
                new_data['salary_max'] = None
                new_data['salary_currency'] = None
            else:
                salary = salary.getText().replace(u'\xa0', u'')
                salary = re.split(r'\s|-', salary)
                if salary[0] == 'до':
                    new_data['salary_min'] = None
                    new_data['salary_max'] = salary[1] + salary[2]
                    new_data['salary_currency'] = salary[3]
                elif salary[0] == 'от':
                    new_data['salary_min'] = salary[1] + salary[2]
                    new_data['salary_max'] = None
                    new_data['salary_currency'] = salary[3]
                elif len(salary) < 4:
                    new_data['salary_min'] = None
                    new_data['salary_max'] = None
                    new_data['salary_currency'] = None

                else:
                    new_data['salary_min'] = salary[0] + salary[1]
                    new_data['salary_max'] = salary[3] + salary[4]
                    new_data['salary_currency'] = salary[5]
            # city = i.find('span', class_='vacancy-serp-item__meta-info').text
            new_data['vacancy_link'] = i.find(class_='bloko-link')['href']
            new_data['site'] = 'hh.ru'
            vak_dict.append(new_data)
        page_num += 1
    return vak_dict


def sj(vac):
    vak_dict = []
    page_num = 0
    while page_num <= 2:
        param = {'keywords': vac, 'profession_only': '1', 'page': page_num}
        header = Headers(headers=True).generate()
        url = 'https://www.superjob.ru/vacancy/search/'
        response = requests.get(url, params=param, headers=header)
        soup = bs(response.text, 'lxml')

        vacancy_items = soup.find_all('div', class_='f-test-search-result-item')
        for i in vacancy_items:
            new_data = {}
            name = i.find(class_='_1rS-s')
            if not name:
                pass
            else:
                new_data['name'] = i.find('div', class_='_1h3Zg _2rfUm _2hCDz _21a7u').text
                new_data['company_name'] = i.find('span', class_='f-test-text-vacancy-item-company-name').text
                city = i.find('span', {'class': 'f-test-text-company-item-location'}).findChildren()[2].getText().split(',')
                new_data['city'] = city[0]
                salary = i.find('span', {'class': '_1h3Zg _2Wp8I _2rfUm _2hCDz _2ZsgW'}).text
                salary = salary.replace(u'\xa0', u' ').split(' ')

                if salary[0] == 'от':
                    new_data['salary_min'] = salary[1]+salary[2]
                    new_data['salary_max'] = None
                    new_data['salary_currency'] = salary[3]
                elif salary[0] == 'до':
                    new_data['salary_min'] = None
                    new_data['salary_max'] = salary[1] + salary[2]
                    new_data['salary_currency'] = salary[3]
                elif len(salary) > 4:
                    new_data['salary_min'] = salary[0] + salary[1]
                    new_data['salary_max'] = salary[3] + salary[4]
                    new_data['salary_currency'] = salary[5]
                else:
                    new_data['salary_min'] = None
                    new_data['salary_max'] = None
                    new_data['salary_currency'] = None
                vacancy_link = i.find('a')['href']
                new_data['vacancy_link'] = f'https://www.superjob.ru{vacancy_link}'
                new_data['site'] = 'superjob.ru'
                vak_dict.append(new_data)
        page_num += 1
    return vak_dict


def vac_parser(vac):
    result = []
    result.extend(hh(vac))
    result.extend(sj(vac))
    return pd.DataFrame(result)


vacancy = 'ИТ Директор'
print(vac_parser(vacancy))
