from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['vakancy']
series_collection = db.vakancy


def find_vak(salary):
    results = series_collection.find({'salary_max': {'$gt': salary}})
    print(results)
    for obj in results:
        print(obj)


find_vak(100000)
