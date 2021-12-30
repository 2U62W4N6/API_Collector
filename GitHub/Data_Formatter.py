from typing import List
import pandas as pd

class Formatter:

    def repositories(self, repos: List[dict]) -> pd.DataFrame:
        repo = pd.DataFrame(repos)
        if not repo.empty:
            repo = pd.concat([repo, repo['node'].apply(pd.Series)], axis=1)
            repo = pd.concat([repo, repo['watchers'].apply(pd.Series).rename(columns={'totalCount' : 'watchersCount'})], axis=1)
            repo = pd.concat([repo, repo['owner'].apply(pd.Series)], axis=1)
            repo = pd.concat([repo, repo['primaryLanguage'].apply(pd.Series).rename(columns={'name' : 'language'})], axis=1)
            repo = repo.drop(columns=['node', 'watchers', 'owner', 'primaryLanguage'])
        return repo
        

    def stars(self, stars: List[dict]) -> pd.DataFrame:
        stars = pd.DataFrame(stars)
        if not stars.empty:
            stars = pd.concat([stars[['id', 'name', 'url']], stars['stars'].apply(pd.Series)], axis=1)
            stars = pd.concat([stars, stars['node'].apply(pd.Series)], axis=1)
            stars = stars.drop(columns=['node'])
        stars = stars.loc[:,~stars.columns.duplicated()]
        return stars

    def forks(self,forks: List[dict]) -> pd.DataFrame:
        forks = pd.DataFrame(forks)
        if not forks.empty:
            forks = pd.concat([forks[['id', 'name', 'url']], forks['forks'].apply(pd.Series)], axis=1)
            forks = pd.concat([forks, forks['node'].apply(pd.Series)], axis=1)
            forks = pd.concat([forks, forks['owner'].apply(pd.Series)], axis=1)
            forks = forks.drop(columns=['node', 'owner'])
        forks = forks.loc[:,~forks.columns.duplicated()]
        return forks

    def watchers(self,watchers: List[dict]) -> pd.DataFrame:
        watchers = pd.DataFrame(watchers)
        if not watchers.empty:
            watchers = pd.concat([watchers[['id', 'name', 'url']], watchers['watchers'].apply(pd.Series)], axis=1)
            watchers = pd.concat([watchers, watchers['node'].apply(pd.Series)], axis=1)
            watchers = watchers.drop(columns=['node'])
        watchers = watchers.loc[:,~watchers.columns.duplicated()]
        return watchers

    def issues(self,issues: List[dict]) -> pd.DataFrame:
        issues = pd.DataFrame(issues)
        if not issues.empty:
            issues = pd.concat([issues[['id', 'name', 'url']], issues['issues'].apply(pd.Series)], axis=1)
            issues = pd.concat([issues, issues['node'].apply(pd.Series)], axis=1)
            issues = pd.concat([issues, issues['comments'].apply(pd.Series).rename(columns={'totalCount' : 'comment_count'})], axis=1)
            issues = pd.concat([issues, issues['author'].apply(pd.Series)], axis=1)
            issues = issues.drop(columns=['node', 'author', 'comments'])
        else:
            issues = issues[['id', 'name', 'url']]
        issues = issues.loc[:,~issues.columns.duplicated()]
        return issues

    def pulls(self,pulls: List[dict]) -> pd.DataFrame:
        pulls = pd.DataFrame(pulls)
        if not pulls.empty:
            pulls = pd.concat([pulls[['id', 'name', 'url']], pulls['pulls'].apply(pd.Series)], axis=1)
            pulls = pd.concat([pulls, pulls['node'].apply(pd.Series)], axis=1)
            pulls = pd.concat([pulls, pulls['author'].apply(pd.Series)], axis=1)
            pulls = pulls.drop(columns=['node', 'author'])
        pulls = pulls.loc[:,~pulls.columns.duplicated()]
        return pulls

    def commits(self,commits: List[dict]) -> pd.DataFrame:
        commits = pd.DataFrame(commits)
        if not commits.empty:
            commits = pd.concat([commits[['id', 'name', 'url']], commits['commits'].apply(pd.Series)], axis=1)
            commits = pd.concat([commits, commits['node'].apply(pd.Series)], axis=1)
            commits = pd.concat([commits, commits['author'].apply(pd.Series).rename(columns={'name' : 'author'})], axis=1)
            commits = commits.drop(columns=['node', 'author'])
        commits = commits.loc[:,~commits.columns.duplicated()]
        return commits




