# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:

    def __init__(self):
        self.client = MongoClient('localhost',27017)
        self.mongo_base = self.client.vacancy_scrapy_hh

    def process_item(self, item, spider):

        collection = self.mongo_base[spider.name]

        if spider.name == 'hhru':

            salary = item['salary']
            item['salary_min'] = None
            item['salary_max'] = None
            item['currency'] = None
            item['gross_net'] = None

            if len(salary) == 7:
                salary_min = int(re.sub('[\D]', '', salary[1]))
                item['salary_min'] = salary_min
                salary_max = int(re.sub('[\D]', '', salary[3]))
                item['salary_max'] = salary_max
                currency = salary[5]
                item['currency'] = currency
                gross_net = salary[6]
                item['gross_net'] = gross_net
                print(salary_min, salary_max, currency, gross_net)
            elif len(salary) == 5:
                if str(salary).find('от') != -1:
                    salary_min = int(re.sub('[\D]', '', salary[1]))
                    item['salary_min'] = salary_min
                    salary_max = None
                    item['salary_max'] = salary_max
                    currency = salary[3]
                    item['currency'] = currency
                    gross_net = salary[4]
                    item['gross_net'] = gross_net
                    print(salary_min, salary_max, currency, gross_net)
                else:
                    salary_min = None
                    item['salary_min'] = salary_min
                    salary_max = int(re.sub('[\D]', '', salary[1]))
                    item['salary_max'] = salary_max
                    currency = salary[3]
                    item['currency'] = currency
                    gross_net = salary[4]
                    item['gross_net'] = gross_net
                    print(salary_min, salary_max, currency, gross_net)

        # del item['salary']
        #print(1)

        else:
            salary = item['salary']
            item['salary_min'] = None
            item['salary_max'] = None
            item['currency'] = None
            item['gross_net'] = None

            if len(salary) == 4:
                salary_min = int(re.sub('[\D]', '', salary[0]))
                item['salary_min'] = salary_min
                salary_max = int(re.sub('[\D]', '', salary[1]))
                item['salary_max'] = salary_max
                currency = salary[3]
                item['currency'] = currency
                gross_net = None
                item['gross_net'] = gross_net
                print(salary_min, salary_max, currency, gross_net)
            elif len(salary) == 3:
                if str(salary).find('от') != -1:
                    salary_min = int(re.sub('[\D]', '', salary[2]))
                    item['salary_min'] = salary_min
                    salary_max = None
                    item['salary_max'] = salary_max
                    currency = re.sub('[0-9]', '', salary[2]).replace('-', '').replace(chr(160), '').replace(chr(32), '')
                    item['currency'] = currency
                    gross_net = None
                    item['gross_net'] = gross_net
                    print(salary_min, salary_max, currency, gross_net)
                else:
                    salary_min = None
                    item['salary_min'] = salary_min
                    salary_max = int(re.sub('[\D]', '', salary[2]))
                    item['salary_max'] = salary_max
                    currency = re.sub('[0-9]', '', salary[2]).replace('-', '').replace(chr(160), '').replace(chr(32), '')
                    item['currency'] = currency
                    gross_net = None
                    item['gross_net'] = gross_net
                    print(salary_min, salary_max, currency, gross_net)


            # print(1)



        collection.insert_one(item)
        return item




    def __del__(self):
        self.client.close()

