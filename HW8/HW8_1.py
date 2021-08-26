import requests
import zipfile
import pandas as pd

url = 'https://op.mos.ru/EHDWSREST/catalog/export/get?id=1197917'
local_file = 'file.zip'
data = requests.get(url)
with open(local_file, 'wb') as file:
    file.write(data.content)

with zipfile.ZipFile('./file.zip','r') as zip_ref:
    zip_ref.extractall('./')

df = pd.read_csv('data-5284-2021-08-19.csv', encoding='1251')
print(df)
df.to_excel('file.xlsx')
