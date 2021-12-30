import pandas as pd

class Formatter:

    def user_objects(self, user_list: dict, account: str) -> pd.DataFrame:
        df = pd.DataFrame(user_list)
        df['account'] = account
        df = pd.concat([df, df["public_metrics"].apply(pd.Series)], axis=1)
        df = df.drop(columns=['public_metrics'])
        df = df.rename(columns={"followers_count": "follower",
                                "following_count": "following",
                                "tweet_count" : "tweet",
                                "listed_count" : "listed"})
        return df

    
    def tweet_objects(self, tweet_list, account: str) -> pd.DataFrame:
        df = pd.DataFrame(tweet_list)
        df['account'] = account
        df = pd.concat([df, df["public_metrics"].apply(pd.Series)], axis=1)
        df['is_retweet'] = df.apply(lambda x:True if 'referenced_tweets' in x else False, axis=1)
        df = df.drop(columns=['public_metrics', 'referenced_tweets'])
        df = df.rename(columns={"retweet_count": "retweets",
                                "reply_count": "replies",
                                "like_count" : "likes",
                                "quote_count" : "quotes"})
        return df
