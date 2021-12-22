from GitHub.API_Requester import Requester
from GitHub.Enum_GitHub import Account_IDs

import json
import time


class Collector:

    def __init__(self, requester: Requester):
        self.requester = requester

    def repositories(self, user_id):
        data = self.requester.get_repository(user_id)
        timestamp = int(time.time())
        counters = []
        traffics = []
        for entry in data:
            entry['contributor'] = self.requester.get_contributos(user_id, entry['name'])
            entry['pulls'] = self.requester.get_pulls(user_id, entry['name'])
            entry['issues'] = self.requester.get_issues(user_id, entry['name'])
            entry['commits'] = self.requester.get_commits(user_id, entry['name'])
            entry['traffic_views'] = self.requester.get_views(user_id, entry['name'])
            entry['traffic_clones'] = self.requester.get_clones(user_id, entry['name'])
            entry['traffic_paths'] = self.requester.get_paths(user_id, entry['name'])
            entry['traffic_referrers'] = self.requester.get_referrers(user_id, entry['name'])
            counter = {
                'timestamp' : timestamp,
                'id' : entry['id'],
                'name' : entry['name'],
                'size' : entry['size'],
                'stargazers_count' : entry['stargazers_count'],
                'watchers_count' : entry['watchers_count'],
                'forks_count' : entry['forks_count'],
                'open_issues_count': entry['open_issues_count'],
                'forks' : entry['forks'],
                'watchers' : entry['watchers'],
                'contributor' : len(entry['contributor']),
                'pulls' : len(entry['pulls']),
                'issues' : len(entry['issues']),
                'commits' : len(entry['commits']),
            }
            counters.append(counter)
            traffic = {
                'timestamp' : timestamp,
                'id' : entry['id'],
                'name' : entry['name'],
                'views' : entry['traffic_views']['views'] if entry['traffic_views'] != None else None,
                'clones' : entry['traffic_clones']["clones"] if entry['traffic_views'] != None else None,
                'popular_paths' : entry['traffic_paths'],
                'referrers' : entry['traffic_referrers']
            }
            traffics.append(traffic)
        return data, counters, traffics

    def discussions(self):
        data = self.requester.get_discussions()
        return data


