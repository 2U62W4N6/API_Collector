from Prodigy.API_Handler import Requester

class Collector:

    def __init__(self, requester: Requester):
        self.requester = requester

    def products(self):
        data = self.requester.get_products()
        return data

    def orders(self):
        data = self.requester.get_orders()
        return data

    def packages(self):
        data = self.requester.get_packages()
        return data
    