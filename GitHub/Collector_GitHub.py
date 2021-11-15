from GitHub.API_GitHub import GitHub
from GitHub.Enum_GitHub import Account_IDs
from keys import GitHub_Keys
import json

account = GitHub(GitHub_Keys.BEARER_TOKEN.value)

def all():
    repositories()
    discussions()

def repositories():
    data = account.get_repository(Account_IDs.EXPLOSION.value)
    for entry in data:
        entry['contributor'] = account.get_contributos(Account_IDs.EXPLOSION.value, entry['name'])
        entry['pulls'] = account.get_pulls(Account_IDs.EXPLOSION.value, entry['name'])
        entry['issues'] = account.get_issues(Account_IDs.EXPLOSION.value, entry['name'])
    remove_urls(data)
    writing(data, 'Repositories')

def remove_urls(data):
    def recursive_remover(data):
        if isinstance(data, dict):
            for key in list(data):
                if isinstance(data[key], dict):
                    recursive_remover(data[key])
                else:
                    if '_url' in key:
                        data.pop(key)
        elif isinstance(data, list):
            for entry in data:
                recursive_remover(entry)

    for entry in data:
        recursive_remover(entry)


def discussions():
    data = account.get_discussions()
    writing(data, 'discussion')

def writing(data, name):
    with open(f'Data/GitHub/{name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)