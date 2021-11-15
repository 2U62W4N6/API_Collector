from API import Base
import requests
import time
import re
from GitHub.Enum_GitHub import API_Endpoint, API_Version

class GitHub(Base):

    def __init__(self, bearer_token):
        self._authentication(bearer_token)
        self.is_valid = self._check_authentication()

    def _authentication(self, bearer_token):
        self._oauth2 = {'Authorization': f'token {bearer_token}'}

    def _check_authentication(self):
        example = 'https://api.github.com/users/explosion/repos'

        oauth2 = requests.get(example, headers=self._oauth2)
        oauth2_status = oauth2.status_code

        print(f'[INFO] Bearer_Token Check: {oauth2_status == 200}')
        
        return oauth2_status == 200
    
    def _check_limit(self, header):
        if not 'X-RateLimit-Remaining' in header:
            return
        elif int(header['X-RateLimit-Remaining']) <= 0:
            duration = int(header['X-RateLimit-Reset']) - int(time.time())
            print(f'[INFO] Rate limit reached for endpoint - sleep for {duration} seconds')
            time.sleep(duration)
        return

    def _pagination(self, url, header, data, response_header):
        if not 'Link' in  response_header:
            return data
        page = re.search('page=\d+(?=>;\srel="next",)', response_header['Link'])
        if page:
            split = page.group().split('=')
            params = { split[0] : split[1]}
            response = requests.get(url, headers=header, params=params)
            data.extend(response.json())
            self._pagination(url, header, data, response.headers)
        return data

    def call_api(self, url, header, params={}):
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

    def get_repository(self, owner):
        url = API_Version.CURRENT.value + API_Endpoint.REPOSITORIES.value.format(owner=owner)
        response, header = self.call_api(url, self._oauth2)
        response = self._pagination(url, self._oauth2, response, header)
        return response

    def get_contributos(self, owner, repository):
        url = API_Version.CURRENT.value + API_Endpoint.CONTRIBUTORS.value.format(
            owner=owner,
            repository=repository
        )
        response, header = self.call_api(url, self._oauth2)
        response = self._pagination(url, self._oauth2, response, header)
        return response

    def get_issues(self, owner, repository):
        url = API_Version.CURRENT.value + API_Endpoint.ISSUES.value.format(
            owner=owner,
            repository=repository
        )
        response, header = self.call_api(url, self._oauth2)
        response = self._pagination(url, self._oauth2, response, header)
        return response

    def get_pulls(self, owner, repository):
        url = API_Version.CURRENT.value + API_Endpoint.PULLS.value.format(
            owner=owner,
            repository=repository
        )
        response, header = self.call_api(url, self._oauth2)
        response = self._pagination(url, self._oauth2, response, header)
        return response

    def get_discussions(self):
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
                        login
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
        response = requests.post(url , headers=self._oauth2 ,json={'query': query, 'variables' : variables})
        data = response.json()['data']['repository']['discussions']['edges']
        self._check_limit(response.headers)
        data = self._graphql_pagination(url, query, self._oauth2, response, data, variables)
        return data


    def _graphql_pagination(self, url, query, header, response, data, variables):
        pageInfo = response.json()['data']['repository']['discussions']['pageInfo']
        if pageInfo['hasNextPage']:
            variables['after'] = pageInfo['endCursor']
            response = requests.post(url , headers=self._oauth2 ,json={'query': query, 'variables' : variables})
            self._check_limit(response.headers)
            if response.status_code == 200:   
                data.extend(response.json()['data']['repository']['discussions']['edges'])
                return self._graphql_pagination(url, query, header, response, data, variables)
            else:
                print('ups')
                print(response.json())
        else:
            return data
