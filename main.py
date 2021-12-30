import concurrent.futures
from concurrent.futures import wait
from twitter.twitter_worker import Worker as twitter
from github.github_worker import Worker as github
from prodigy.prodigy_worker import Worker as prodigy
from module.logging import LogHandler


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

    github_job()
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        t1 = executor.submit(twitter_job)
        t2 = executor.submit(github_job)
        t3 = executor.submit(prodigy_job)
        wait(t1)
        wait(t2)
        wait(t3)
        print(f'[LOGS] : DEBUG: {LogHandler.COUNT[10]} | INFO : {LogHandler.COUNT[20]} | WARNING : {LogHandler.COUNT[30]} | ERROR : {LogHandler.COUNT[40]} | CRITICAL: {LogHandler.COUNT[50]}')


