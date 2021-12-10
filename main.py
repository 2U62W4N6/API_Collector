from Twitter.Twitter_Worker import Worker as twitter
from GitHub.GitHub_Worker import Worker as github
from Prodigy.Prodigy_Worker import Worker as prodigy

if __name__ == '__main__':
    twitter_worker = twitter()
    twitter_worker.run()

    github_worker = github()
    github_worker.run()

    prodigy_workter = prodigy()
    prodigy_workter.run()


