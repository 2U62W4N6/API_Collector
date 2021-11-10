import enum

class API_Version(enum.Enum):
    CURRENT = 'https://api.github.com/'
    GRAPHQL = "https://api.github.com/graphql"

class API_Endpoint(enum.Enum):
    REPOSITORIES = 'users/{owner}/repos'
    ISSUES = "repos/{owner}/{repo}/issues"
    PULLS = "repos/{owner}/{repo}/pulls"

class Account_IDs(enum.Enum):
    EXPLOSION = "explosion"
