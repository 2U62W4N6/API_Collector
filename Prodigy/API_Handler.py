from Prodigy.Enum_Prodigy import API_Endpoint, API_Version
from API import Base
import requests
import time

class Requester(Base):
    """
    Twitter API Class with all necessary methods.

    Args:
        bearer_token (str) : Bearer Token for OAuth2
        api_key (str) : API Key for OAuth1
        api_key_secret (str) : API Key Secret for OAuth1
        access_token (str) : Access Token key for OAuth1
        access_token_secret (str) : Access Token Secret key for OAuth1
    """
    def __init__(self, key, secret):
        self._authentication(key, secret)
        self.is_valid = self._check_authentication()


    def _authentication(self, key, secret):
        """
        Method to create authentication attributes which are provided in each request.

        Args:
            bearer_token (str) : Bearer Token for OAuth2
            api_key (str) : API Key for OAuth1
            api_key_secret (str) : API Key Secret for OAuth1
            access_token (str) : Access Token key for OAuth1
            access_token_secret (str) : Access Token Secret key for OAuth1
        """
        self.url = f'https://{key}:{secret}@www.sendowl.com/api/'



    def _check_authentication(self):
        """
        Method to check authentication on a example-request for Auth.
        No requests can be made if the check fails.
        """
        example = self.url + 'v1/products'
        header = {"Accept": "application/json"} 
        auth = requests.get(example, headers=header)

        print(f'[INFO] Authentication Check: {auth.status_code == 200}')
        
        return auth.status_code == 200



    def _check_limit(self):
        """
        Method to handle API Limitation.
        Checks whether remaining request can still be made or to wait until the next window opens 
        """
        time.sleep(2)
        return

    
        
    def api_get(self, url, header, params={}):
        """
        Method to handle API Requests.
        
        Args:
            url (str) : the endpoint of the API
            auth (OAuth1) : OAuth1 authentication initialized by the OAuth1 class
            header (dict) : header for the request, also includes the OAuth2 authentication
            params (dict) : paramter to add a request query

        Return:
            response (dict) : returns the respoonse if status code = 200, else None
        """
        if not self.is_valid:
            return
        
        response = requests.get(url, headers=header, params=params)
        status_code = response.status_code
        print(url, params, f'[{status_code}]')

        self._check_limit()
        
        if status_code == 200:
            return response.json()
        else:
            return None



    def get_products(self):
        """
        Retrieve all followers for the given user id

        Args:
            user_id (str) : id of the twitter account

        Return:
            list[dict] : returns a list of user-dicts
        """
        
        header = {"Accept": "application/json"} 
        url = self.url + API_Version.OLD.value + API_Endpoint.PRODUCTS.value
        response = self.api_get(url, header)
        return response



    def get_orders(self):
        """
        Retrieve all following (friends) for the given user id

        Args:
            user_id (str) : id of the twitter account

        Return:
            list[dict] : returns a list of user-dicts
        """
        header = {"Accept": "application/json"} 
        params = {
            'sort':'newest_first',
            'per_page': 50,
            'page': 1
        }
        url = self.url + API_Version.CURRENT.value + API_Endpoint.ORDERS.value
        
        response = self.api_get(url, header, params)
        return self._pagination(url, header, params, response)


    def get_packages(self):
        header = {"Accept": "application/json"} 

        url = self.url + API_Version.OLD.value + API_Endpoint.PACKAGES.value
        response = self.api_get(url, header)
        return  response


    def _pagination(self, url, header, params, response):
        """
        Recursive Function
        Iterates over the pages and retrive all data points
        Args:
            url (str) : the endpoint of the API
            auth (OAuth1) : OAuth1 authentication initialized by the OAuth1 class
            response_header (dict) : header for the request, also includes the OAuth2 authentication
            params (dict) : paramter to add a request query
            data (list) : the data list from the response
            meta (dict) : the meta information from the response

        Return:
            list(dict) : returns a list of response objects (user, tweet)
        """
        data = response
        while (len(response) == 50):
            params['page'] = params['page'] + 1
            response = self.api_get(url, header, params)
            data.extend(response)
        return data
   