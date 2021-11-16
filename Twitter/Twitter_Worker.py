from Twitter.API_Handler import Requester
from Twitter.Data_Collector import Collector
from Twitter.Data_Formatter import Formatter
from Twitter.Enum_Twitter import Account_IDs
import json

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

            self.formatter.user_objects(follower)
            self.formatter.user_objects(following)
            self.formatter.tweet_objects(tweets)

            self.write(follower, f"{account.name}_Follower")
            self.write(following, f"{account.name}_Following")
            self.write(tweets, f"{account.name}_Tweets")


    def write(self, data, name):
        with open(f'Data/Twitter/{name}.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        

