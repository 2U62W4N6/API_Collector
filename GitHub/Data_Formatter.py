

class Formatter:

    
    def discussion(self, discussions):
        for discussion in discussions:
            discussion = discussion['node']
            discussion['comments_count'] = discussion['comments']['totalCount']
            discussion.pop('comments')
            discussion['labels'] = [node['node'].get('name') for node in discussion['labels']['edges']] if len(discussion['labels']['edges']) > 0 else []
            discussion['answer_createdAt'] = discussion['answer'].get('createdAt') if discussion['answer'] != None else None
            discussion.pop('answer')
            discussion['author'] = discussion['author'].get('url') if discussion['author'] != None else None
            discussion['isAnswerable'] = discussion['category'].get('isAnswerable') if discussion['category'] != None else None
            discussion['category'] = discussion['category'].get('name') if discussion['category'] != None else None
        return list(entry['node'] for entry in discussions)

    def repositories(self, repositories):
        for repo in repositories:
            self.remove_urls(repo)
            self.remove_urls(repo['owner'])
            for contributor in repo['contributor']:
                self.remove_urls(contributor)
            for issue in repo['issues']:
                if 'user' in issue:
                    issue['user'] = issue['user']['html_url']
                self.remove_urls(issue)
                
            for commit in repo['commits']:
                commit.pop('url', None)
                commit.pop('commiter', None)
                self.remove_urls(commit['author'])
            for pull in repo['pulls']:
                self.remove_urls(pull['user'])
                pull.pop('base', None)
                pull.pop('_link', None)
                pull.pop('head', None)


    def remove_urls(self, dictionary):
        if dictionary == None:
            return
        for key in list(dictionary):
            if '_url' in key and 'html_url' not in key:
                dictionary.pop(key)   


