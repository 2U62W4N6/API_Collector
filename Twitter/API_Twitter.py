from API import Base
import requests
from requests_oauthlib import OAuth1
import time


class Twitter(Base):

    def __init__(self, bearer, api_key, api_key_secret, access_token, access_token_secret):
        self.authentication(bearer, api_key, api_key_secret, access_token, access_token_secret)
        self.is_valid = self._check_authentication()

    def _check_authentication(self):
        example = 'https://api.twitter.com/2/tweets/1261326399320715264'

        oauth1 = requests.get(example, auth=self._oauth1)
        oauth1_status = oauth1.status_code
        
        oauth2 = requests.get(example, headers=self._oauth2)
        oauth2_status = oauth2.status_code

        print(f'[INFO] Authentication Check: {oauth1_status == 200}')
        print(f'[INFO] Bearer_Token Check: {oauth2_status == 200}')
        
        return oauth1_status == 200 and oauth2_status == 200

    def _check_limit(self, header):

        if not 'x-rate-limit-remaining' in header:
            return
        elif int(header['x-rate-limit-remaining']) <= 0:
            duration = int(header['x-rate-limit-reset']) - int(time.time())
            print(f'[INFO] Rate limit reached for endpoint - sleep for {duration} seconds')
            time.sleep(duration)
        return

    def authentication(self, bearer, api_key, api_key_secret, access_token, access_token_secret):
        self._oauth1 = OAuth1(api_key, api_key_secret, access_token, access_token_secret)
        self._oauth2 = {'Authorization' : f'Bearer {bearer}'}
        
    def call_api(self, url, header='', params=''):
        if not self.is_valid:
            return
        
        response = requests.get(url, headers=header, params=params)
        status_code = response.status_code
        print(url, params, f'[{status_code}]')

        self._check_limit(response.headers)
        
        if status_code == 200:
            return response.json()
        else:
            return None

