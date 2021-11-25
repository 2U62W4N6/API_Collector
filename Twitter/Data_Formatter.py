
class Formatter:

    def user_objects(self, user_list):
        for user in user_list:
            if 'public_metrics' in user:
                user['followers_count'] = user['public_metrics']['followers_count']
                user['following_count'] = user['public_metrics']['following_count']
                user['tweet_count']  = user['public_metrics']['tweet_count']
                user['listed_count'] = user['public_metrics']['listed_count']
                user.pop('public_metrics')

    
    def tweet_objects(self, tweet_list):
        for tweet in tweet_list:
            if 'retweet' in tweet.keys():
                tweet['retweeted_at'] = tweet['created_at']
                tweet['created_at'] = tweet['retweet']['created_at']
                tweet['retweet_id'] = tweet['retweet']['id']
                tweet['is_retweet'] = True
                tweet['retweet_count'] = tweet['retweet']['public_metrics']['retweet_count']
                tweet['reply_count'] = tweet['retweet']['public_metrics']['reply_count']
                tweet['like_count'] = tweet['retweet']['public_metrics']['like_count']
                tweet['quote_count'] = tweet['retweet']['public_metrics']['quote_count']
                tweet.pop('retweet')
                tweet.pop('referenced_tweets')
            else:
                tweet['is_retweet'] = False
                tweet['retweet_id'] = None
                tweet['retweet_count'] = tweet['public_metrics']['retweet_count']
                tweet['reply_count'] = tweet['public_metrics']['reply_count']
                tweet['like_count'] = tweet['public_metrics']['like_count']
                tweet['quote_count'] = tweet['public_metrics']['quote_count']
            tweet.pop('public_metrics')
