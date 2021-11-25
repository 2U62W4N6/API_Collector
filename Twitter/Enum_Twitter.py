import enum

class API_Version(enum.Enum):
    OLD =  'https://api.twitter.com/1.1/',
    CURRENT = 'https://api.twitter.com/2/'

class API_Endpoint(enum.Enum):
    TWEET = 'tweets/{id}'
    TWEETS = 'users/{id}/tweets'
    FOLLOWER = 'users/{id}/followers'
    FOLLOWING = 'users/{id}/following'
    MENTIONS = 'users/{id}/mentions'
    LIKED_BY = 'tweets/{id}/liking_users'
    RETWEETED_BY = 'tweets/{id}/retweeted_by'

class Account_IDs(enum.Enum):
    EXPLOSION = 744095828013424640
    SPACY = 3422200198
