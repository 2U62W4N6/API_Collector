from twitter.enum_twitter import API_Endpoint, API_Version
from requests_oauthlib import OAuth1
from api import API
import requests
import time
from typing import Union, Optional, List
from module.logging import LOGGER_DEBUG, LOGGER_INFO, LOGGER_WARNING, LOGGER_ERROR, LOGGER_CRITICAL 


class Requester(API):
    """
    Twitter API Class with all necessary methods.

    Args:
        bearer_token (str) : Bearer Token for OAuth2
        api_key (str) : API Key for OAuth1
        api_key_secret (str) : API Key Secret for OAuth1
        access_token (str) : Access Token key for OAuth1
        access_token_secret (str) : Access Token Secret key for OAuth1
    """
    def __init__(self, 
                bearer_token: str,
                api_key: str,
                api_key_secret: str,
                access_token: str,
                access_token_secret: str):
                
        self._authentication(bearer_token, api_key, api_key_secret, access_token, access_token_secret)
        self.is_valid = self._check_authentication()



    def _authentication(self,
                        bearer_token: str,
                        api_key: str,
                        api_key_secret: str,
                        access_token: str,
                        access_token_secret: str
                        ) -> None:
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



    def _check_authentication(self) -> bool:
        """
        Method to check authentication on a example-request for OAuth1 and OAuth2.
        No requests can be furhter made if the check fails.
        """
        example = 'https://api.twitter.com/2/tweets/1261326399320715264'

        oauth1 = requests.get(example, auth=self._oauth1)
        oauth1_status = oauth1.status_code
        
        oauth2 = requests.get(example, headers=self._oauth2)
        oauth2_status = oauth2.status_code
        
        if oauth1_status == 200 and oauth2_status == 200:
            LOGGER_INFO.log('[TWITTER] Credential-Check: OK')
            return True
        else:
            LOGGER_CRITICAL.log('[TWITTER] Credential-Check: WRONG | check or update provided keys and token in the .env file')
            return False
        



    def _check_limit(self, header: dict) -> None:
        """
        Method to handle API Limitation.
        Checks whether remaining request can still be made or to wait until the next window opens 
        """
        rate_limit_remaining = header.get('x-rate-limit-remaining', None)
        if rate_limit_remaining:
            if int(rate_limit_remaining) <= 0:
                window = header['x-rate-limit-reset']
                duration = int(window) - int(time.time())
                LOGGER_INFO.log(f'[TWITTER] Rate Limit Reached: Sleep for {duration} Seconds')
                time.sleep(duration + 1)
        return

    
        
    def call_api(self,
                url: str,
                auth: OAuth1,
                header: dict,
                params: dict={}
                ) -> Optional[Union[dict, List[dict]]]:
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
        

        self._check_limit(response.headers)

        message = f'{url} | {params} | [{status_code}]'
        if status_code == 200:
            LOGGER_INFO.log(message)
            return response.json()
        else:
            LOGGER_WARNING.log(message)
            LOGGER_WARNING.log(response.json())
            return None

    def _payload(self, response: requests.Response) -> Optional[Union[dict, List[dict]]]:
        return response.get('data', None)

    def _pagination(self,
                    url: str,
                    auth: OAuth1,
                    response_header: dict,
                    params: dict,
                    data: Optional[Union[dict, List[dict]]],
                    meta: dict
                    ) ->  Optional[Union[dict, List[dict]]]:
        """
        Recursive Function
        Iterates over the pages and retrive all data points
        Args:
            url (str) : the endpoint of the API
            auth (OAuth1) : OAuth1 authentication initialized by the OAuth1 class
            response_header (dict) : header for the request, also includes the OAuth2 authentication
            params (dict) : paramter to add a request query
            data (list) : the data from the response
            meta (dict) : the meta information from the response

        Return:
            list(dict) : returns a list of response objects (user, tweet)
        """
        if 'next_token' in meta:
            params['pagination_token'] = meta['next_token']
            response = self.call_api(url, auth, response_header, params)
            data.extend(self._payload(response))
            meta = response['meta']
            self._pagination(url, auth, response_header, params, data, meta)
        return data
   


    def get_follower(self, user_id: Union[int, str]) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve all followers for the given user id

        Args:
            user_id (int | str) : id of the twitter account

        Return:
            list[dict] : returns a list of user-dicts
        """
        url = API_Version.CURRENT.value + API_Endpoint.FOLLOWER.value.format(id=user_id)
        params = {
            'max_results' : 1000,
            'user.fields' : 'public_metrics,profile_image_url'
        }
        response = self.call_api(url, self._oauth1, self._oauth2, params)
        return self._pagination(url, self._oauth1, self._oauth2, params, self._payload(response), response['meta'])



    def get_following(self, user_id: Union[int, str]) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve all following (friends) for the given user id

        Args:
            user_id (int | str) : id of the twitter account

        Return:
            list[dict] : returns a list of user-dicts
        """
        url = API_Version.CURRENT.value + API_Endpoint.FOLLOWING.value.format(id=user_id)
        params = {
            'max_results' : 1000,
            'user.fields' : 'public_metrics,profile_image_url'
        }
        response = self.call_api(url, self._oauth1, self._oauth2, params)
        return self._pagination(url, self._oauth1, self._oauth2, params, self._payload(response), response['meta'])



    def get_tweets(self, user_id: Union[int, str]) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve all tweets for the given user id

        Args:
            user_id (int | str) : id of the twitter account

        Return:
            list[dict] : returns a list of tweet-dicts
        """
        url = API_Version.CURRENT.value + API_Endpoint.TWEETS.value.format(id=user_id)
        params = {
            'max_results' : 100,
            'tweet.fields' : 'public_metrics,created_at,author_id',
            'expansions' : 'referenced_tweets.id,author_id',
            'user.fields' : 'username',
        }
        response = self.call_api(url, self._oauth1, self._oauth2, params)
        return self._pagination(url, self._oauth1, self._oauth2, params, self._payload(response), response['meta'])



    def get_tweet(self, tweet_id: Union[int, str]) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve a tweet for the given tweet id

        Args:
            user_id (int | str) : id of the twitter account

        Return:
            (dict) : returns a tweet
        """
        url = API_Version.CURRENT.value + API_Endpoint.TWEET.value.format(id=tweet_id)
        params = {
            'tweet.fields' : 'public_metrics,created_at',
            'expansions':'author_id',
            'user.fields' : 'username',
        }
        response = self.call_api(url, self._oauth1, self._oauth2, params)
        return self._payload(response)



    def get_liked_by(self, tweet_id: Union[int, str]) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve a list of user who liked a tweet, for the given tweet id

        Args:
            user_id (int | str) : id of the twitter account

        Return:
            list[dict] : returns a list of tweet-dicts
        """
        url = API_Version.CURRENT.value + API_Endpoint.LIKED_BY.value.format(id=tweet_id)
        response = self.call_api(url, self._oauth1, self._oauth2)
        return self._payload(response)



    def get_retweeted_by(self, tweet_id: Union[int, str]) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve a list of user who retweeted a tweet, for the given tweet id

        Args:
            user_id (int | str) : id of the twitter account

        Return:
            list[dict] : returns a list of user-dicts
        """
        url = API_Version.CURRENT.value + API_Endpoint.RETWEETED_BY.value.format(id=tweet_id)
        response = self.call_api(url, self._oauth1, self._oauth2)
        return self._payload(response)


    