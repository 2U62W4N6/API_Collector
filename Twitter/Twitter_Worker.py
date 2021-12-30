from twitter.api_handler import Requester
from twitter.data_collector import Collector
from twitter.data_formatter import Formatter
from twitter.enum_twitter import Account_IDs

import time
import os.path as path
import pandas as pd

import os
from dotenv import load_dotenv
load_dotenv()


class Worker:
    """
    Twitter Worker who does all the main work.

    It creates three main components:
    - requester (Requester): which brings all functions to perform the api calls
    - collector (Collector): enables the requester to make those api calls
    - formatter (Formatter): process the payload from the api into csv file
    """

    def __init__(self):
        self.requester = Requester(os.getenv('TWITTER_BEARER_TOKEN'),
                                os.getenv('TWITTER_API_KEY'),
                                os.getenv('TWITTER_API_KEY_SECRET'),
                                os.getenv('TWITTER_ACCESS_TOKEN'),
                                os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))
        self.collector = Collector(self.requester)
        self.formatter = Formatter()
       
    def run(self):
        # Exit thread if the credentials are not valid
        if not self.requester.is_valid:
            return


        # Creates placeholder dataframes
        all_follower = pd.DataFrame({})
        all_following = pd.DataFrame({})
        all_tweets = pd.DataFrame({})
        follower_timeline = pd.DataFrame({})
        following_timeline = pd.DataFrame({})


        # Load timeline data if they exist (new rows will be appended)
        if path.exists('Data/Twitter/Follower_Timelines.csv'):
            follower_timeline = pd.read_csv('Data/Twitter/Follower_Timeline.csv')
        if path.exists('Data/Twitter/Following_Timelines.csv'):
            following_timeline = pd.read_csv('Data/Twitter/Following_Timeline.csv')


        # Iterate over each account which are stored in the ENUM file
        for account in Account_IDs:
            # Request all data
            follower = self.collector.follower(account.value)
            following = self.collector.following(account.value)
            tweets = self.collector.tweets(account.value)
            
            # Format all data
            follower = self.formatter.user_objects(follower, account.name)
            following = self.formatter.user_objects(following, account.name)
            tweets = self.formatter.tweet_objects(tweets, account.name)

            # Add a new column to specify the twitter account and append it to the main dataframe
            all_follower =  pd.concat([all_follower, follower])
            all_following =  pd.concat([all_following, following])
            all_tweets =  pd.concat([all_tweets, tweets])

            # Create a new row for the timelines
            timestamp = int(time.time())
            follower_timeline_row = {
                'timestamp' : timestamp,
                'account_id' : account.value,
                'account_name' : account.name,
                'follower' : len(follower)
            }
 
            following_timeline_row = {
               'timestamp' : timestamp,
               'account_id' : account.value,
               'account_name' : account.name,
               'following' : len(following)
            }

            # Append the new created rows to the timeline
            follower_timeline = follower_timeline.append(follower_timeline_row, ignore_index=True)
            following_timeline = following_timeline.append(following_timeline_row, ignore_index=True)


        # Write all data 
        all_follower.to_csv('Data/Twitter/Follower.csv')
        all_following.to_csv('Data/Twitter/Following.csv')
        all_tweets.to_csv('Data/Twitter/Tweets.csv')
        follower_timeline.to_csv('Data/Twitter/Follower_Timeline.csv')
        following_timeline.to_csv('Data/Twitter/Following_Timeline.csv')

        


        

