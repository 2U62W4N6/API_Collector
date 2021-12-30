from github.api_handler import Requester
import pandas as pd
import time


class Collector:

        
    all_forks = pd.DataFrame({})
    all_watchers = pd.DataFrame({})
    all_pulls = pd.DataFrame({})
    all_issues = pd.DataFrame({})
    all_commits = pd.DataFrame({})

    def __init__(self, requester: Requester):
        self.requester = requester

    def repositories(self, owner:str):
        repos = self.requester.get_repositories(owner)
        return repos

    def stars(self, owner: str, repos: list):
        all_stars = []
        for repo in repos:
            all_stars.append(self.requester.get_stars(owner, repo))
        return all_stars

    def watchers(self, owner: str, repos: list):
        all_watchers = []
        for repo in repos:
            all_watchers.append(self.requester.get_watchers(owner, repo))
        return all_watchers

    def forks(self, owner: str, repos: list):
        all_forks = []
        for repo in repos:
            all_forks.append(self.requester.get_forks(owner, repo))
        return all_forks

    def issues(self, owner: str, repos: list):
        all_issues = []
        for repo in repos:
            all_issues.append(self.requester.get_issues(owner, repo))
        return all_issues

    def pulls(self, owner: str, repos: list):
        all_pulls = []
        for repo in repos:
            all_pulls.append(self.requester.get_pulls(owner, repo))
        return all_pulls

    def commits(self, owner: str, repos: list):
        all_commits = []
        for repo in repos:
            all_commits.append(self.requester.get_commits(owner, repo))
        return all_commits
    