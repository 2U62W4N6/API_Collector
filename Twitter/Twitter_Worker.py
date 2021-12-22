from Twitter.API_Handler import Requester
from Twitter.Data_Collector import Collector
from Twitter.Data_Formatter import Formatter
from Twitter.Enum_Twitter import Account_IDs
import json
import time

import os
from dotenv import load_dotenv
load_dotenv()


class Worker:

    def __init__(self):
        self.requester = Requester(os.getenv('TWITTER_BEARER_TOKEN'),
                                os.getenv('TWITTER_API_KEY'),
                                os.getenv('TWITTER_API_KEY_SECRET'),
                                os.getenv('TWITTER_ACCESS_TOKEN'),
                                os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
        self.collector = Collector(self.requester)
        self.formatter = Formatter()
       
    def run(self):
        for account in Account_IDs:
            follower = self.collector.follower(account.value)
            following = self.collector.following(account.value)
            tweets = self.collector.tweets(account.value)
            timestamp = int(time.time())
            #self.formatter.user_objects(follower)
            #self.formatter.user_objects(following)
            #self.formatter.tweet_objects(tweets)

            follower_count = {
                'timestamp' : timestamp,
               'account_id' : account.value,
               'account_name' : account.name,
               'follower' : len(follower)
            }

            following_count = {
               'timestamp' : timestamp,
               'account_id' : account.value,
               'account_name' : account.name,
               'follower' : len(following)
            }

            self.update(follower_count, 'Twitter_Follower_Progression')
            self.update(following_count, 'Twitter_Following_Progression')
            self.write(follower, f"{account.name}_Follower")
            self.write(following, f"{account.name}_Following")
            self.write(tweets, f"{account.name}_Tweets")


    def write(self, data, name):
        with open(f'Data/Twitter/{name}.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def update(self, data, name):
        with open(f'Data/Twitter/{name}.json', "r+") as f:
            current = json.load(f)
            current.append(data)
            f.seek(0)
            json.dump(current, f, indent=4)
        

