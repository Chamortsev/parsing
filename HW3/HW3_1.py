from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
import requests
import re
from fake_headers import Headers

client = MongoClient('localhost', 27017)
db = client['vakancy']
series_collection = db.vakancy



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
                    new_data['salary_max'] = int(salary[1] + salary[2])
                    new_data['salary_currency'] = salary[3]
                elif salary[0] == 'от':
                    new_data['salary_min'] = int(salary[1] + salary[2])
                    new_data['salary_max'] = None
                    new_data['salary_currency'] = salary[3]
                elif len(salary) < 4:
                    new_data['salary_min'] = None
                    new_data['salary_max'] = None
                    new_data['salary_currency'] = None

                else:
                    new_data['salary_min'] = int(salary[0] + salary[1])
                    new_data['salary_max'] = int(salary[3] + salary[4])
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
                    new_data['salary_min'] = int(salary[1]+salary[2])
                    new_data['salary_max'] = None
                    new_data['salary_currency'] = salary[3]
                elif salary[0] == 'до':
                    new_data['salary_min'] = None
                    new_data['salary_max'] = int(salary[1] + salary[2])
                    new_data['salary_currency'] = salary[3]
                elif len(salary) > 4:
                    new_data['salary_min'] = int(salary[0] + salary[1])
                    new_data['salary_max'] = int(salary[3] + salary[4])
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


vacancy = 'ИТ Директор'

series_collection.delete_many({})


def insert_document(collection, data):
    return collection.insert_one(data).inserted_id


for i in hh(vacancy):
    insert_document(series_collection, i)

for i in sj(vacancy):
    insert_document(series_collection, i)
