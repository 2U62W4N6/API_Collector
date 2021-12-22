from Prodigy.API_Handler import Requester
from Prodigy.Data_Collector import Collector
from Prodigy.Data_Formatter import Formatter

import json

import os
from dotenv import load_dotenv
load_dotenv()


class Worker:

    def __init__(self):
        self.requester = Requester(os.getenv('PRODIGY_KEY'),
                                os.getenv('PRODIGY_SECRET'))
        self.collector = Collector(self.requester)
        self.formatter = Formatter()
       
    def run(self):
        product = self.collector.products()
        orders = self.collector.orders()
        packages = self.collector.packages()

        #self.formatter.order_object(orders)

        self.write(product, f"Prodigy_Products")
        self.write(orders, f"Prodigy_Orders")
        self.write(packages, f"Prodigy_Packages")


    def write(self, data, name):
        with open(f'Data/Prodigy/{name}.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        

