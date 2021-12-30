from twitter.api_handler import Requester
 

class Collector:

    def __init__(self, requester: Requester):
        self.requester = requester

    def follower(self, user_id):
        data = self.requester.get_follower(user_id)
        return data

    def following(self, user_id):
        data = self.requester.get_following(user_id)
        return data

    def tweets(self, user_id):
        data = self.requester.get_tweets(user_id)
        return data

