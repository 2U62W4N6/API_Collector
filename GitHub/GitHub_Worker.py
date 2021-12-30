from github.api_handler import Requester
from github.data_collector import Collector
from github.data_formatter import Formatter
from github.enum_github import Account_IDs
import pandas as pd

import os
from dotenv import load_dotenv
load_dotenv()

class Worker:
    """
    GitHub Worker who does all the main work.

    It creates three main components:
    - requester (Requester): which brings all functions to perform the api calls
    - collector (Collector): enables the requester to make those api calls
    - formatter (Formatter): process the payload from the api into csv file
    """

    def __init__(self):
        self.requester = Requester(os.getenv('GITHUB_BEARER_TOKEN'))
        self.collector = Collector(self.requester)
        self.formatter = Formatter()
       
    def run(self):
        # Exit thread if the credentials are not valid
        if not self.requester.is_valid:
            return

        owner = Account_IDs.EXPLOSION.value

        # Request all data
        repos = self.collector.repositories(owner)
        repos = self.formatter.repositories(repos)
        repo_list = repos['name'].tolist()
        
        stars = self.collector.stars(owner, repo_list)
        forks = self.collector.stars(owner, repo_list)
        watchers = self.collector.stars(owner, repo_list)
        pulls = self.collector.stars(owner, repo_list)
        issues = self.collector.stars(owner, repo_list)
        commits = self.collector.stars(owner, repo_list)

        # need to update formatter class
        stars = pd.DataFrame(stars)
        forks =  pd.DataFrame(forks)
        watchers = pd.DataFrame(watchers)
        pulls = pd.DataFrame(pulls)
        issues =pd.DataFrame(issues)
        commits  =pd.DataFrame(commits)
        
        stars.to_csv('Data/GitHub/Stars.csv')
        forks.to_csv('Data/GitHub/Forks.csv') 
        watchers.to_csv('Data/GitHub/Watchers.csv')
        pulls.to_csv('Data/GitHub/Pulls.csv')
        issues.to_csv('Data/GitHub/Issues.csv')
        commits.to_csv('Data/GitHub/Commits.csv')
        


