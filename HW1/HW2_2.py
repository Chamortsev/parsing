# 2. Изучить список открытых API. Найти среди них любое,
# требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
from json import loads, dump
from requests import post

clientId = '836'
apikey = '0296d4f2-70a1-4c09-b507-904fd05567b9'
url = 'https://cb-api.ozonru.me/v1/product/list'
p = 1
response = post(url, verify=True, timeout=None, headers={
    'Client-Id': clientId, 'Api-Key': apikey, 'Content-Type': 'application/json'},
                json={

                    "filter": {
                        "offer_id": [

                        ],
                        "product_id": [

                        ],
                        "visibility": "ALL"
                    },
                    "page": p,
                    "page_size": 10

                }
                )
res = response.status_code
data = loads(response.content)
data = data['result']['items']

with open('hw1_2.json', 'w') as f:
    f.write('PageCode ')
    dump(res, f)
    f.write('\n')
    dump(data, f)
