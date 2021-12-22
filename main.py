from Twitter.Twitter_Worker import Worker as twitter
from GitHub.GitHub_Worker import Worker as github
from Prodigy.Prodigy_Worker import Worker as prodigy
import concurrent.futures


if __name__ == '__main__':
    def twitter_job():
        twitter_worker = twitter()
        twitter_worker.run()

    def github_job():
        github_worker = github()
        github_worker.run()

    def prodigy_job():
        prodigy_workter = prodigy()
        prodigy_workter.run()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(twitter_job)
        executor.submit(github_job)
        executor.submit(prodigy_job)


