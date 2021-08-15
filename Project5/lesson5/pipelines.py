# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
import re


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):
        item['max_salary'] = 0
        item['min_salary'] = 0
        item['currency'] = 0

        if spider.name == 'hhru':
            item['site'] = 'hh.ru'
            if len(item['salary']) > 1:
                salary_split = item['salary'].split(" ")

                if salary_split[0] == 'от':
                    item['max_salary'] = None
                    item['min_salary'] = int(re.sub('\D', "", salary_split[1]))
                    item['currency'] = salary_split[2].replace(".", "")

                elif salary_split[0] == 'до':
                    item['min_salary'] = None
                    item['max_salary'] = int(re.sub('\D', "", salary_split[1]))
                    item['currency'] = salary_split[2].replace(".", "")

                else:
                    salary2split = salary_split[0].split("-")
                    if len(salary2split) > 1:
                        item['min_salary'] = int(re.sub('\D', "", salary2split[0]))
                        item['max_salary'] = int(re.sub('\D', "", salary2split[1]))
                        item['currency'] = salary_split[1].replace(".", "")

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
