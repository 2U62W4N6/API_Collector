from Twitter.API_Twitter import Twitter
from Twitter.Enum_Twitter import Account_IDs
from keys import Twitter_Keys
import json

bearer = Twitter_Keys.BEARER_TOKEN.value
api_key = Twitter_Keys.API_KEY.value
api_key_secret = Twitter_Keys.API_KEY_SECRET.value
access_token = Twitter_Keys.ACCESS_TOKEN.value
access_token_secret = Twitter_Keys.ACCESS_TOKEN_SECRET.value
connection = Twitter(bearer, api_key, api_key_secret, access_token, access_token_secret)

def all():
    follower()
    following()
    tweets()

def follower():
    data = connection.get_follower(Account_IDs.EXPLOSION.value)
    writing(data, f'{Account_IDs.EXPLOSION.name}_follower')

def following():
    data = connection.get_following(Account_IDs.EXPLOSION.value)
    writing(data, f'{Account_IDs.EXPLOSION.name}_following')

def tweets():
    tweets = connection.get_tweets(Account_IDs.EXPLOSION.value)
    
    def update(tweet):
        if 'referenced_tweets' in tweet:
            tweet['retweet'] = True
            response = connection.get_tweet(tweet['referenced_tweets'][0]['id'])
            tweet['public_metrics'] = response['public_metrics']
            tweet['retweeted_at'] = tweet['created_at'] 
            tweet['created_at'] = response['created_at']

            tweet['liked_by'] = connection.get_liked_by(tweet['referenced_tweets'][0]['id'])
            tweet['retweeted_by'] = connection.get_retweeted_by(tweet['referenced_tweets'][0]['id'])
        else:
            tweet['retweet'] = False
            tweet['liked_by'] = connection.get_liked_by(tweet['id'])
            tweet['retweeted_by'] = connection.get_retweeted_by(tweet['id'])

        return tweet

    data = list(map(update, tweets))
    writing(data, f'{Account_IDs.EXPLOSION.name}_tweets')

    
def writing(data, name):
    with open(f'Data/Twitter/{name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)