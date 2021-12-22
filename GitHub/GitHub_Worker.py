from GitHub.API_Requester import Requester
from GitHub.Data_Collecter import Collector
from GitHub.Data_Formatter import Formatter
from GitHub.Enum_GitHub import Account_IDs
import json

import os
from dotenv import load_dotenv
load_dotenv()


class Worker:

    def __init__(self):
        self.requester = Requester(os.getenv('GITHUB_BEARER_TOKEN'))
        self.collector = Collector(self.requester)
        self.formatter = Formatter()
       
    def run(self):
        for account in Account_IDs:
            repositories, counters, traffics = self.collector.repositories(account.value)
            #self.formatter.repositories(repositories)
            self.write(repositories, f"{account.name}_Repositories")
            self.update(counters, f'{account.name}_GitHub_Counters_Progression')
            self.update(traffics, f'{account.name}_GitHub_Traffic_Progression')
        discussions = self.collector.discussions()
        #discussions = self.formatter.discussion(discussions)
        self.write(discussions, "SPACY_Discussion")


    def write(self, data, name):
        with open(f'Data/GitHub/{name}.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def update(self, data, name):
        with open(f'Data/GitHub/{name}.json', "r+") as f:
            current = json.load(f)
            current.extend(data)
            f.seek(0)
            json.dump(current, f, indent=4)
        

