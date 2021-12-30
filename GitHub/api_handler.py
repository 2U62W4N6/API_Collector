from typing import Optional, Union, List
from api import API
import requests
import time
from github import queries
from github.enum_github import API_Endpoint, API_Version
from module.logging import LOGGER_DEBUG, LOGGER_INFO, LOGGER_WARNING, LOGGER_ERROR, LOGGER_CRITICAL 

class Requester(API):
    """
    GitHub API Class with all necessary methods.

    Args:
        bearer_token (str) : Bearer Token for OAuth2
    """
    def __init__(self, bearer_token: str):
        self._authentication(bearer_token)
        self.is_valid = self._check_authentication()



    def _authentication(self, bearer_token: str):
        """
        Method to create authentication attributes which are provided in each request.

        Args:
            bearer_token (str) : Bearer Token for OAuth2
        """
        self._oauth2 = {'Authorization': f'token {bearer_token}'}



    def _check_authentication(self) -> bool:
        """
        Method to check authentication on a example-request for OAuth2.
        No requests can be made if the check fails.
        """
        example = 'https://api.github.com/users/explosion/repos'

        oauth2 = requests.get(example, headers=self._oauth2)
        oauth2_status = oauth2.status_code
        
        if oauth2_status == 200:
            LOGGER_INFO.log('[GITHUB] Credential-Check: OK')
            return True
        else:
            LOGGER_CRITICAL.log('[GITHUB] Credential-Check: WRONG | check or update provided keys and token in the .env file')
            return False
    


    def _check_limit(self, header: dict):
        """
        Method to handle API Limitation.
        Checks whether remaining request can still be made or to wait until the next window opens 
        """
        rate_limit_remaining = header.get('X-RateLimit-Remaining', None)
        if rate_limit_remaining:
            if int(rate_limit_remaining) <= 0:
                window = header['X-RateLimit-Reset']
                duration = int(window) - int(time.time())
                LOGGER_INFO.log(f'[GITHUB] Rate Limit Reached: Sleep for {duration} Seconds')
                time.sleep(duration + 1)
        return



    def _pagination(self, url :str, header: dict, data: Optional[Union[dict, List[dict]]], response_header: dict):
        """
        Not needed here
        """
        pass



    def call_api(self, url: str, header: dict, params: dict={}) -> Optional[Union[dict, List[dict]]]:
        """
        Method to handle API GET-Requests.
        
        Args:
            url (str) : the endpoint of the API
            header (dict) : header for the request, also includes the OAuth2 authentication
            params (dict) : paramter to add a request query

        Return:
            response (dict) : returns the respoonse if status code = 200, else None
        """
        if not self.is_valid:
            return
        
        response = requests.get(url, headers=header, params=params)
        status_code = response.status_code
        self._check_limit(response.headers)

        message = f'{url} | {params} | [{status_code}]'
        if status_code == 200:
            LOGGER_INFO.log(message)
            return response.json(), response.headers
        else:
            LOGGER_WARNING.log(message)
            LOGGER_WARNING.log(response.json())
            return None, response.headers
            


    def api_post(self, url: str, body: str, params: dict={}) -> Optional[Union[dict, List[dict]]]:
        """
        Method to handle API POST-Requests.
        
        Args:
            url (str) : the endpoint of the API
            header (dict) : header for the request, also includes the OAuth2 authentication
            body (dict) : the body to be sent with the post request
            params (dict) : paramter to add a request query

        Return:
            response (dict) : returns the respoonse if status code = 200, else None
        """
        if not self.is_valid:
            return
        
        response = requests.post(url, json=body, headers=self._oauth2, params=params)
        status_code = response.status_code
        self._check_limit(response.headers)

        message = f'{url} | {body["variables"]} | [{status_code}]'
        if status_code == 200:
            LOGGER_INFO.log(message)
            return response.json(), response.headers
        else:
            LOGGER_WARNING.log(message)
            LOGGER_WARNING.log(response.json())
            return None, response.headers





    def get_clones(self, owner: str, repository: str) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve a list of clone count 
        Args:
            owner : name of the repo owner
            repository : name of the repo
        Return:
            returns a list of clone count
        """
        url = API_Version.CURRENT.value + API_Endpoint.TRAFFIC_CLONES.value.format(
            owner=owner,
            repository=repository
        )
        response, _ = self.api_get(url, self._oauth2)
        return response



    def get_views(self, owner: str, repository: str) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve a list of view count 
        Args:
            owner : name of the repo owner
            repository : name of the repo
        Return:
            returns a list of view count
        """
        url = API_Version.CURRENT.value + API_Endpoint.TRAFFIC_VIEWS.value.format(
            owner=owner,
            repository=repository
        )
        response, _ = self.api_get(url, self._oauth2)
        return response



    def get_paths(self, owner: str, repository: str) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve a list of popular paths (which sites are mostly visited)
        Args:
            owner : name of the repo owner
            repository : name of the repo
        Return:
            returns a list of popular paths
        """
        url = API_Version.CURRENT.value + API_Endpoint.TRAFFIC_PATHS.value.format(
            owner=owner,
            repository=repository
        )
        response, _ = self.api_get(url, self._oauth2)
        return response



    def get_referrers(self, owner: str, repository: str) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve a list of top referrers (from which sites the visitor come from)
        Args:
            owner : name of the repo owner
            repository : name of the repo
        Return:
            returns a list of top referrers
        """
        url = API_Version.CURRENT.value + API_Endpoint.TRAFFIC_REFERRERS.value.format(
            owner=owner,
            repository=repository
        )
        response, _ = self.api_get(url, self._oauth2)
        return response



    def get_repositories(self, owner: str) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve a list of discussion from the spacy repository

        Args:
            owner : name of the owner
        Return:
            returns a list of repositories
        """
        url = API_Version.GRAPHQL.value
        variables = {
            "n" : 100,
            "user" : f"user:{owner}"
        } 
        query = queries.REPOSITORIES
        response, _ = self.api_post(url, body={'query': query, 'variables' : variables})
        return response['data']['search']['edges']
        

    def get_stars(self, owner: str, repository: str) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve stargazer timeline
        Args:
            owner : name of the repo owner
            repository : name of the repo
        Return:
            returns a list of stargazers
        """
        url = API_Version.GRAPHQL.value
        variables = {
            "n" : 100,
            "owner" : owner,
            "name" : repository
        } 
        query = queries.STARS
        repo = None
        stars = []
        while True:
            response, _ = self.api_post(url, body={'query': query, 'variables' : variables})
            repo = response['data']['repository'].copy()
            repo.pop('stargazers')
            stars.extend(response['data']['repository']['stargazers']['edges'])
            meta = response['data']['repository']['stargazers']['pageInfo']
            if meta['hasNextPage']:
                variables['cursor'] = meta['endCursor']
            else:
                break
        repo['stars'] = stars
        return repo




    def get_forks(self, owner: str, repository: str) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve fork timeline
        Args:
            owner : name of the repo owner
            repository : name of the repo
        Return:
            returns a list of forks
        """
        url = API_Version.GRAPHQL.value
        variables = {
            "n" : 100,
            "owner" : owner,
            "name" : repository
        } 
        query = queries.FORKS
        repo = None
        forks = []
        while True:
            response, _ = self.api_post(url, body={'query': query, 'variables' : variables})
            if response != None:
                repo = response['data']['repository'].copy()
                repo.pop('forks')
                forks.extend(response['data']['repository']['forks']['edges'])
                meta = response['data']['repository']['forks']['pageInfo']
                if meta['hasNextPage']:
                    variables['cursor'] = meta['endCursor']
                else:
                    break
        repo['forks'] = forks
        return repo



    def get_watchers(self, owner: str, repository: str) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve watchhers timeline
        Args:
            owner : name of the repo owner
            repository : name of the repo
        Return:
            returns a list of watchers
        """
        url = API_Version.GRAPHQL.value
        variables = {
            "n" : 100,
            "owner" : owner,
            "name" : repository
        } 
        query = queries.WATCHERS
        repo = None
        watchers = []
        while True:
            response, _ = self.api_post(url, body={'query': query, 'variables' : variables})
            if response != None:
                repo = response['data']['repository'].copy()
                repo.pop('watchers')
                watchers.extend(response['data']['repository']['watchers']['edges'])
                meta = response['data']['repository']['watchers']['pageInfo']
                if meta['hasNextPage']:
                    variables['cursor'] = meta['endCursor']
                else:
                    break
        repo['watchers'] = watchers
        return repo




    def get_commits(self, owner: str, repository: str) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve commit timeline
        Args:
            owner : name of the repo owner
            repository : name of the repo
        Return:
            returns a list of commits
        """
        url = API_Version.GRAPHQL.value
        variables = {
            "n" : 100,
            "owner" : owner,
            "name" : repository
        } 
        query = queries.COMMITS
        repo = None
        commits = []
        while True:
            response, _ = self.api_post(url, body={'query': query, 'variables' : variables})
            repo = response['data']['repository'].copy()
            repo.pop('defaultBranchRef')
            commits.extend(response['data']['repository']['defaultBranchRef']['target']['history']['edges'])
            meta = response['data']['repository']['defaultBranchRef']['target']['history']['pageInfo']
            if meta['hasNextPage']:
                variables['cursor'] = meta['endCursor']
            else:
                break
        repo['commits'] = commits
        return repo

    def get_pulls(self, owner: str, repository: str) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve pullrequests timeline
        Args:
            owner : name of the repo owner
            repository : name of the repo
        Return:
            returns a list of pullrequests
        """
        url = API_Version.GRAPHQL.value
        variables = {
            "n" : 100,
            "owner" : owner,
            "name" : repository
        } 
        query = queries.PULLS
        repo = None
        pulls = []
        while True:
            response, _ = self.api_post(url, body={'query': query, 'variables' : variables})
            repo = response['data']['repository'].copy()
            repo.pop('pullRequests')
            pulls.extend(response['data']['repository']['pullRequests']['edges'])
            meta = response['data']['repository']['pullRequests']['pageInfo']
            
            if meta['hasNextPage']:
                variables['cursor'] = meta['endCursor']
            else:
                break
        repo['pulls'] = pulls
        return repo


    
    def get_issues(self, owner: str, repository: str) -> Optional[Union[dict, List[dict]]]:
        """
        Retrieve issues timeline
        Args:
            owner : name of the repo owner
            repository : name of the repo
        Return:
            returns a list of pullrequests
        """
        url = API_Version.GRAPHQL.value
        variables = {
            "n" : 100,
            "owner" : owner,
            "name" : repository
        } 
        query = queries.ISSUES
        repo = None
        issues = []
        while True:
            response, _ = self.api_post(url, body={'query': query, 'variables' : variables})
            repo = response['data']['repository'].copy()
            repo.pop('issues')
            issues.extend(response['data']['repository']['issues']['edges'])
            meta = response['data']['repository']['issues']['pageInfo']
            if meta['hasNextPage']:
                variables['cursor'] = meta['endCursor']
            else:
                break
        repo['issues'] = issues
        return repo

  