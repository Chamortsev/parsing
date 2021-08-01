# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

from requests import get
from json import loads, dump

url = 'https://api.github.com'
user = 'Chamortsev'
response = get(f'{url}/users/{user}/repos')

data = loads(response.content)

for my_dict in data:
    status = my_dict['name']
    print(my_dict['name'])

with open('HW1_1.json', 'w') as f:
    dump(response.json(), f)
