#import Twitter.Collector_Twitter as twitter
from GitHub.API_GitHub import GitHub
import pypistats
"""

if __name__ == '__main__':
    #twitter.all()

    
    test = GitHub('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')
    data = test.get_repos('explosion')
    print(len(data))
"""
print(pypistats.recent("spacy", "week", format="json"))
