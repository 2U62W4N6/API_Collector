import enum

class API_Version(enum.Enum):
    CURRENT = 'https://api.github.com/'
    GRAPHQL = "https://api.github.com/graphql"

class API_Endpoint(enum.Enum):
    REPOSITORIES = 'users/{owner}/repos'
    CONTRIBUTORS = 'repos/{owner}/{repository}/contributors'
    ISSUES = "repos/{owner}/{repository}/issues"
    PULLS = "repos/{owner}/{repository}/pulls"
    COMMITS = 'repos/{owner}/{repository}/commits'
    TRAFFIC_CLONES = 'repos/{owner}/{repository}/traffic/clones'
    TRAFFIC_VIEWS = 'repos/{owner}/{repository}/traffic/views'
    TRAFFIC_PATHS = 'repos/{owner}/{repository}/traffic/popular/paths'
    TRAFFIC_REFERRERS = 'repos/{owner}/{repository}/traffic/popular/referrers'


class Account_IDs(enum.Enum):
    EXPLOSION = "explosion"
