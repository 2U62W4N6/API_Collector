from GitHub.API_Requester import Requester
from GitHub.Enum_GitHub import Account_IDs

import json


class Collector:

    def __init__(self, requester: Requester):
        self.requester = requester

    def repositories(self, user_id):
        data = self.requester.get_repository(user_id)
        for entry in data:
            entry['contributor'] = self.requester.get_contributos(user_id, entry['name'])
            entry['pulls'] = self.requester.get_pulls(user_id, entry['name'])
            entry['issues'] = self.requester.get_issues(user_id, entry['name'])
            entry['commits'] = self.requester.get_commits(user_id, entry['name'])
            entry['traffic_views'] = self.requester.get_views(user_id, entry['name'])
            entry['traffic_clones'] = self.requester.get_clones(user_id, entry['name'])
            entry['traffic_paths'] = self.requester.get_paths(user_id, entry['name'])
            entry['traffic_referrers'] = self.requester.get_referrers(user_id, entry['name'])
        return data

    def discussions(self):
        data = self.requester.get_discussions()
        return data


