
from prodigy.enum_prodigy import API_Endpoint, API_Version
from api import API
import requests
import time
from typing import Union, Optional, List
from module.logging import LOGGER_DEBUG, LOGGER_INFO, LOGGER_WARNING, LOGGER_ERROR, LOGGER_CRITICAL 

class Requester(API):
    """
    Prodigy API Class with all necessary methods.

    Args:
        api_key : API Key for OAuth1
        api_key_secret : API Key Secret for OAuth1
    """
    def __init__(self, key, secret):
        self.header = {"Accept": "application/json"} 
        self._authentication(key, secret)
        self.is_valid = self._check_authentication()


    def _authentication(self, key: str, secret: str):
        """
        Method to create authentication attributes which are provided in each request.

        Args:
            api_key : API Key for OAuth1
            api_key_secret  : API Key Secret for OAuth1
        """
        self.url = f'https://{key}:{secret}@www.sendowl.com/api/'



    def _check_authentication(self) -> bool:
        """
        Method to check authentication on a example-request for Auth.
        No requests can be made if the check fails.
        """
        example = self.url + 'v1/products'
        response = requests.get(example, headers=self.header)
        status_code = response.status_code
        if status_code == 200:
            LOGGER_INFO.log('[PRODIGY] Credential-Check: OK')
            return True
        else:
            LOGGER_CRITICAL.log('[PRODIGY] Credential-Check: WRONG | check or update provided keys and token in the .env file')
            return False
        




    def _check_limit(self):
        """
        Method to handle API Limitation.
        SendOwl doesn't have a limitation rule, but it is adviced to prevent spam-requesting (may result to an ip-ban)
        """
        duration = 2
        time.sleep(duration)
        return

    
        
    def call_api(self, url:str, params: dict={}) -> Optional[Union[dict, List[dict]]]:
        """
        Method to handle API Requests.
        
        Args:
            url : the endpoint of the API
            params : paramter to add a request query

        Return:
            returns the respoonse if status code = 200, else None
        """
        if not self.is_valid:
            return
        
        response = requests.get(url, headers=self.header, params=params) 
        status_code = response.status_code

        self._check_limit()
        
        message = f'{url} | {params} | [{status_code}]'
        if status_code == 200:
            LOGGER_INFO.log(message)
            return response.json()
        else:
            LOGGER_WARNING.log(message)
            LOGGER_WARNING.log(response.json())
            return None

    def _payload(self, response:  Optional[Union[dict, List[dict]]], key: str) -> Optional[Union[dict, List[dict]]]:
        """
        Not needed, the payload is just the response.json()
        """
        pass


    def _pagination(self, url: str, params: dict, data: Optional[Union[dict, List[dict]]]) -> Optional[Union[dict, List[dict]]]:
        """
        Loop Function
        Iterates over the pages and retrive all data points
        Args:
            url : the endpoint of the API
            params : paramter to add a request query
            data : the data list from the response

        Return:
            list(dict) : returns a list of response objects (orders)
        """
        all_data = data
        response = data
        while (len(response) == 50):
            params['page'] += 1
            response = self.call_api(url, params)
            all_data.extend(response)
        return all_data

    
    def get_products(self) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve all products from prodigy

        Return:
            a list of product-dicts
        """
        
        
        url = self.url + API_Version.OLD.value + API_Endpoint.PRODUCTS.value
        response = self.call_api(url)
        return response



    def get_orders(self) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve all orders from prodigy

        Return:
           a list of order-dicts
        """
        params = {
            'sort':'newest_first',
            'per_page': 50,
            'page': 1
        }
        url = self.url + API_Version.CURRENT.value + API_Endpoint.ORDERS.value
        
        response = self.call_api(url, params)
        return self._pagination(url, params, response)



    def get_packages(self) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve all packages from prodigy

        Return:
            a list of packages-dicts
        """
        url = self.url + API_Version.OLD.value + API_Endpoint.PACKAGES.value
        response = self.call_api(url)
        return  response


    
   