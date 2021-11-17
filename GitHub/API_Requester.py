from API import Base
import requests
import time
import re
from GitHub.Enum_GitHub import API_Endpoint, API_Version

class Requester(Base):
    """
    GitHub API Class with all necessary methods.

    Args:
        bearer_token (str) : Bearer Token for OAuth2
    """
    def __init__(self, bearer_token):
        self._authentication(bearer_token)
        self.is_valid = self._check_authentication()



    def _authentication(self, bearer_token):
        """
        Method to create authentication attributes which are provided in each request.

        Args:
            bearer_token (str) : Bearer Token for OAuth2
        """
        self._oauth2 = {'Authorization': f'token {bearer_token}'}



    def _check_authentication(self):
        """
        Method to check authentication on a example-request for OAuth2.
        No requests can be made if the check fails.
        """
        example = 'https://api.github.com/users/explosion/repos'

        oauth2 = requests.get(example, headers=self._oauth2)
        oauth2_status = oauth2.status_code

        print(f'[INFO] Bearer_Token Check: {oauth2_status == 200}')
        
        return oauth2_status == 200
    


    def _check_limit(self, header):
        """
        Method to handle API Limitation.
        Checks whether remaining request can still be made or to wait until the next window opens 
        """
        if not 'X-RateLimit-Remaining' in header:
            return
        elif int(header['X-RateLimit-Remaining']) <= 0:
            duration = int(header['X-RateLimit-Reset']) - int(time.time())
            print(f'[INFO] Rate limit reached for endpoint - sleep for {duration} seconds')
            time.sleep(duration)
        return



    def _pagination(self, url, header, data, response_header):
        """
        Recursive Function
        Iterates over the pages and retrive all data points
        Args:
            url (str) : the endpoint of the API
            header (dict) : header for the request, also includes the OAuth2 authentication
            params (dict) : paramter to add a request query
            data (list) : the data list from the response
            meta (dict) : the meta information from the response

        Return:
            list(dict) : returns a list of response objects (user, tweet)
        """
        if not 'Link' in response_header:
            return data
        page = re.search('page=\d+(?=>;\srel="next",)', response_header['Link'])
        if page:
            split = page.group().split('=')
            params = {split[0] : split[1]}
            response, header = self.api_get(url, header=header, params=params)
            data.extend(response)
            self._pagination(url, self._oauth2, data, header)
        return data



    def api_get(self, url, header, params={}):
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
        print(url, params, f'[{status_code}]')
        self._check_limit(response.headers)

        if status_code == 200:
            return response.json(), response.headers
        else:
            return None
        


    def api_post(self, url, header, body, params={}):
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
        
        response = requests.post(url, json=body, headers=header, params=params)
        status_code = response.status_code
        print(url, params, f'[{status_code}]')
        self._check_limit(response.headers)

        if status_code == 200:
            return response.json(), response.headers
        else:
            return None



    def get_repository(self, owner):
        """
        Retrieve a list of repositories for the given owner

        Args:
            owner (str) : name of the repository owner

        Return:
            list[dict] : returns a list of repository-dicts
        """
        url = API_Version.CURRENT.value + API_Endpoint.REPOSITORIES.value.format(owner=owner)
        response, header = self.api_get(url, self._oauth2)
        response = self._pagination(url, self._oauth2, response, header)
        return response



    def get_contributos(self, owner, repository):
        """
        Retrieve a list of user who contribute to the repository

        Args:
            owner (str) : name of the repository owner
            repository (str) : name of the repository
        Return:
            list[dict] : returns a list of user-dicts
        """
        url = API_Version.CURRENT.value + API_Endpoint.CONTRIBUTORS.value.format(
            owner=owner,
            repository=repository
        )
        response, header = self.api_get(url, self._oauth2)
        response = self._pagination(url, self._oauth2, response, header)
        return response



    def get_issues(self, owner, repository):
        """
        Retrieve a list of issues from the repository

        Args:
            owner (str) : name of the repository owner
            repository (str) : name of the repository
        Return:
            list[dict] : returns a list of issue-dicts
        """
        url = API_Version.CURRENT.value + API_Endpoint.ISSUES.value.format(
            owner=owner,
            repository=repository
        )
        response, header = self.api_get(url, self._oauth2)
        response = self._pagination(url, self._oauth2, response, header)
        return response



    def get_pulls(self, owner, repository):
        """
        Retrieve a list of pull requests from the repository

        Args:
            owner (str) : name of the repository owner
            repository (str) : name of the repository
        Return:
            list[dict] : returns a list of pull_request-dicts
        """
        url = API_Version.CURRENT.value + API_Endpoint.PULLS.value.format(
            owner=owner,
            repository=repository
        )
        response, header = self.api_get(url, self._oauth2)
        response = self._pagination(url, self._oauth2, response, header)
        return response



    def get_commits(self, owner, repository):
        """
        Retrieve a list of commits from the repository

        Args:
            owner (str) : name of the repository owner
            repository (str) : name of the repository
        Return:
            list[dict] : returns a list of commit-dicts
        """
        url = API_Version.CURRENT.value + API_Endpoint.COMMITS.value.format(
            owner=owner,
            repository=repository
        )
        response, header = self.api_get(url, self._oauth2)
        response = self._pagination(url, self._oauth2, response, header)
        return response



    def get_discussions(self):
        """
        Retrieve a list of discussion from the spacy repository

        Return:
            list[dict] : returns a list of discussion-dicts
        """
        url = API_Version.GRAPHQL.value
        variables = {
            "n" : 100
        } 
        query = """
        query($n: Int, $after: String){ 
            repository(name:"spacy", owner:"explosion"){
                discussions(first: $n, after : $after){
                pageInfo {
                    endCursor
                    hasNextPage
                    hasPreviousPage
                }
                edges{
                    node{
                    id
                    url
                    comments{totalCount}
                    createdAt
                    publishedAt
                    labels(first: 20){
                    edges{
                        node
                            {name}
                        }
                    }
                    answerChosenAt
                    answer{createdAt}
                    title
                    url
                    author{
                        url
                    }
                    category{
                        isAnswerable
                        name
                    }
                    }
                }
                }
            }
        }
        """
        response, _ = self.api_post(url, header=self._oauth2, body={'query': query, 'variables' : variables})
        data = response['data']['repository']['discussions']['edges']
        data = self._graphql_pagination(url, query, self._oauth2, response, data, variables)
        return data



    def _graphql_pagination(self, url, query, header, response, data, variables):
        """
        Recursive Function
        Iterates over the pages and retrive all data points
        Args:
            url (str) : the endpoint of the API
            header (dict) : header for the request, also includes the OAuth2 authentication
            response (dict) : response data from the request
            data (list) : the data from all responses
            variables (dict) : variables to modify query, which includes pagination

        Return:
            list(dict) : returns a list of response objects (user, tweet)
        """
        pageInfo = response['data']['repository']['discussions']['pageInfo']
        if pageInfo['hasNextPage']:
            variables['after'] = pageInfo['endCursor']
            response, _ = self.api_post(url, header=self._oauth2, body={'query': query, 'variables' : variables})
            data.extend(response['data']['repository']['discussions']['edges'])
            return self._graphql_pagination(url, query, header, response, data, variables)
        else:
            return data
