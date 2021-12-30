from prodigy.api_handler import Requester
from prodigy.data_collector import Collector
from prodigy.data_formatter import Formatter

import pandas as pd


import os
from dotenv import load_dotenv
load_dotenv()


class Worker:
    """
    Prodigy Worker who does all the main work.

    It creates three main components:
    - requester (Requester): which brings all functions to perform the api calls
    - collector (Collector): enables the requester to make those api calls
    - formatter (Formatter): process the payload from the api into csv file
    """
    def __init__(self):
        self.requester = Requester(os.getenv('PRODIGY_KEY'),
                                os.getenv('PRODIGY_SECRET'))
        self.collector = Collector(self.requester)
        self.formatter = Formatter()
       
    def run(self):
        # Exit thread if the credentials are not valid
        if not self.requester.is_valid:
            return

        # Request all data
        product = self.collector.products()
        orders = self.collector.orders()
        packages = self.collector.packages()

        # Format all data
        product = pd.DataFrame(product)
        packages = pd.DataFrame(packages)
        orders, carts = self.formatter.order_object(orders)

        # Write all data 
        carts.to_csv('Data/Prodigy/Carts.csv')
        product.to_csv('Data/Prodigy/Products.csv')
        packages.to_csv('Data/Prodigy/Packages.csv')
        orders.to_csv('Data/Prodigy/Orders.csv')


        

