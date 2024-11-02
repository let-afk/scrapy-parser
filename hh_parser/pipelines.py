# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import regex


class HhParserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancy

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        new_item = self.create_new_item(item)
        collection.insert_one(new_item)
        return new_item

    @staticmethod
    def create_new_item(item):
        new_item = item.deepcopy()
        del new_item["salary"]
        new_item["min_salary"] = None
        new_item["max_salary"] = None
        new_item["cur"] = None
        if item["salary"]:
            salary = [s.replace(u'\xa0', '') for s in item["salary"]]
            for ind, s in enumerate(salary):
                if s.isdigit():
                    if salary[ind - 1].strip() == 'от':
                        new_item["min_salary"] = int(s)
                    elif salary[ind - 1].strip() == 'до':
                        new_item["max_salary"] = int(s)
            new_item["cur"] = regex.findall(r'\p{Sc}', "".join(item["salary"]))[0]
        return new_item
