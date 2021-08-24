"""
2. Написать программу, которая собирает «Хиты продаж» с сайтов техники М.видео, ОНЛАЙН ТРЕЙД и складывает данные в БД.
Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары.
"""

import selenium.common.exceptions
from selenium import webdriver
import time
from pymongo import MongoClient
driver = webdriver.Chrome('chromedriver.exe')

client = MongoClient('localhost', 27017)
db = client['hits']
series_collection = db.hits

url = 'https://www.onlinetrade.ru'
driver.get(url)
time.sleep(1)
# try:
#
#     buton = driver.find_element_by_xpath('/html/body/div[5]/div/div[1]/span')
#     buton.click()
# except selenium.common.exceptions.NoSuchElementExeption:
#     pass

links = [i.get_attribute('href') for i in driver.find_elements_by_css_selector('#tabs_hits div.indexGoods__item__flexCover a')]

unique_links = set(links)

products = {}
for i in unique_links:
    driver.get(i)
    time.sleep(1)
    products['name'] = driver.find_element_by_css_selector('div.productPage__card h1').text
    products['article'] = driver.find_element_by_class_name('catalog__displayedItem__storeCode ').text
    products['price'] = driver.find_element_by_class_name('catalog__displayedItem__actualPrice').text
    products['description'] = driver.find_element_by_class_name('descr__columnCell').text
    series_collection.insert_one(products)
    products = {}
driver.quit()
