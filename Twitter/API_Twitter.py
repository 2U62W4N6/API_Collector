from Twitter.Enum_Twitter import API_Endpoint, API_Version
from requests_oauthlib import OAuth1
from API import Base
import requests
import time

class Twitter(Base):
    """
    Twitter API Class with all necessary methods.

    Args:
        bearer_token (str) : Bearer Token for OAuth2
        api_key (str) : API Key for OAuth1
        api_key_secret (str) : API Key Secret for OAuth1
        access_token (str) : Access Token key for OAuth1
        access_token_secret (str) : Access Token Secret key for OAuth1
    """
    def __init__(self, bearer_token, api_key, api_key_secret, access_token, access_token_secret):
        self.authentication(bearer_token, api_key, api_key_secret, access_token, access_token_secret)
        self.is_valid = self._check_authentication()



    def _authentication(self, bearer_token, api_key, api_key_secret, access_token, access_token_secret):
        """
        Method to create authentication attributes which are provided in each request.

        Args:
            bearer_token (str) : Bearer Token for OAuth2
            api_key (str) : API Key for OAuth1
            api_key_secret (str) : API Key Secret for OAuth1
            access_token (str) : Access Token key for OAuth1
            access_token_secret (str) : Access Token Secret key for OAuth1
        """
        self._oauth1 = OAuth1(api_key, api_key_secret, access_token, access_token_secret)
        self._oauth2 = {'Authorization' : f'Bearer {bearer_token}'}



    def _check_authentication(self):
        """
        Method to check authentication on a example-request for OAuth1 and OAuth2.
        No requests can be made if the check fails.
        """
        example = 'https://api.twitter.com/2/tweets/1261326399320715264'

        oauth1 = requests.get(example, auth=self._oauth1)
        oauth1_status = oauth1.status_code
        
        oauth2 = requests.get(example, headers=self._oauth2)
        oauth2_status = oauth2.status_code

        print(f'[INFO] Authentication Check: {oauth1_status == 200}')
        print(f'[INFO] Bearer_Token Check: {oauth2_status == 200}')
        
        return oauth1_status == 200 and oauth2_status == 200



    def _check_limit(self, header):
        """
        Method to handle API Limitation.
        Checks whether remaining request can still be made or to wait until the next window opens 
        """
        if not 'x-rate-limit-remaining' in header:
            return
        elif int(header['x-rate-limit-remaining']) <= 0:
            duration = int(header['x-rate-limit-reset']) - int(time.time())
            print(f'[INFO] Rate limit reached for endpoint - sleep for {duration} seconds')
            time.sleep(duration)
        return

    
        
    def call_api(self, url, auth, header, params={}):
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
        
        response = requests.get(url, auth=auth, headers=header, params=params)
        status_code = response.status_code
        print(url, params, f'[{status_code}]')

        self._check_limit(response.headers)
        
        if status_code == 200:
            return response.json()
        else:
            return None



    def get_follower(self, user_id):
        """
        Retrieve all followers for the given user id

        Args:
            user_id (str) : id of the twitter account

        Return:
            list[dict] : returns a list of user-dicts
        """
        url = API_Version.CURRENT.value + API_Endpoint.FOLLOWER.value.format(id=user_id)
        params = {
            'max_results' : 1000,
            'user.fields' : 'public_metrics'
        }
        response = self.call_api(url, self._oauth1, self._oauth2, params)
        return self._pagination(url, self._oauth1, self._oauth2, params, response['data'], response['meta'])



    def get_following(self, user_id):
        """
        Retrieve all following (friends) for the given user id

        Args:
            user_id (str) : id of the twitter account

        Return:
            list[dict] : returns a list of user-dicts
        """
        url = API_Version.CURRENT.value + API_Endpoint.FOLLOWING.value.format(id=user_id)
        params = {
            'max_results' : 1000,
            'user.fields' : 'public_metrics'
        }
        response = self.call_api(url, self._oauth1, self._oauth2, params)
        return self._pagination(url, self._oauth1, self._oauth2, params, response['data'], response['meta'])



    def get_tweets(self, user_id):
        """
        Retrieve all tweets for the given user id

        Args:
            user_id (str) : id of the twitter account

        Return:
            list[dict] : returns a list of tweet-dicts
        """
        url = API_Version.CURRENT.value + API_Endpoint.TWEETS.value.format(id=user_id)
        params = {
            'max_results' : 100,
            'tweet.fields' : 'public_metrics,created_at',
            'expansions' : 'referenced_tweets.id'
        }
        response = self.call_api(url, self._oauth1, self._oauth2, params)
        return self._pagination(url, self._oauth1, self._oauth2, params, response['data'], response['meta'])



    def get_tweet(self, tweet_id):
        """
        Retrieve a tweet for the given tweet id

        Args:
            user_id (str) : id of the twitter account

        Return:
            (dict) : returns a tweet
        """
        url = API_Version.CURRENT.value + API_Endpoint.TWEET.value.format(id=tweet_id)
        params = {
            'tweet.fields' : 'public_metrics,created_at'
        }
        response = self.call_api(url, self._oauth1, self._oauth2, params)
        return response['data'] if 'data' in response else {}



    def get_liked_by(self, tweet_id):
        """
        Retrieve a list of user who liked a tweet, for the given tweet id

        Args:
            user_id (str) : id of the twitter account

        Return:
            list[dict] : returns a list of tweet-dicts
        """
        url = API_Version.CURRENT.value + API_Endpoint.LIKED_BY.value.format(id=tweet_id)
        response = self.call_api(url, self._oauth1, self._oauth2)
        return response['data'] if 'data' in response else {}



    def get_retweeted_by(self, tweet_id):
        """
        Retrieve a list of user who liked a tweet, for the given tweet id

        Args:
            user_id (str) : id of the twitter account

        Return:
            list[dict] : returns a list of user-dicts
        """
        url = API_Version.CURRENT.value + API_Endpoint.RETWEETED_BY.value.format(id=tweet_id)
        response = self.call_api(url, self._oauth1, self._oauth2)
        return response['data'] if 'data' in response else {}



    def _pagination(self, url, auth, header, params, data, meta):
        """
        Recursive Function
        Iterates over the possible pages and retrive all data points
        Args:
            url (str) : the endpoint of the API
            auth (OAuth1) : OAuth1 authentication initialized by the OAuth1 class
            header (dict) : header for the request, also includes the OAuth2 authentication
            params (dict) : paramter to add a request query
            data (list) : the data list from the response
            meta (dict) : the meta information from the response

        Return:
            list(dict) : returns a list of response objects (user, tweet)
        """
        if 'next_token' in meta:
            params['pagination_token'] = meta['next_token']
            response = self.call_api(url, auth, header, params)
            data.extend(response['data'])
            meta = response['meta']
            self._pagination(url, auth, header, params, data, meta)
        return data
   