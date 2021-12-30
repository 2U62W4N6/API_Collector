
REPOSITORIES = """
query Repositories($user: String!, $n: Int!, $cursor: String) {
    search(first: $n, after: $cursor, type: REPOSITORY, query: $user) {
        edges {
            node {
                ... on Repository {
                    id
                    name
                    url
                    forkCount
                    watchers {
                        totalCount
                    }
                    stargazerCount
                    owner {
                        login
                    }
                    createdAt
                    updatedAt
                    primaryLanguage {
                        name
                    }
                }
            }
        }
        pageInfo {
            endCursor
            hasNextPage
        }
    }
}
"""

ISSUES = """
query Issues($owner: String!, $name: String!, $n: Int, $cursor: String) {
    repository(owner: $owner, name: $name) {
        id
        name
        url
        issues(first: $n, after: $cursor) {
            edges {
                node {
                    id
                    body
                    url
                    createdAt
                    updatedAt
                    closedAt
                    state
                    comments {
                        totalCount
                    }
                    author {
                        login
                    }
                }
            }
            pageInfo {
                endCursor
                hasNextPage
            }
        } 
    }
}
"""

PULLS = """
query Pulls($owner: String!, $name: String!, $n: Int, $cursor: String) {
    repository(owner: $owner, name: $name) {
        id
        name
        url
        pullRequests(first: $n, after: $cursor) { 
            edges {
                node {
                    id
                    author {
                        login
                    }
                    url
                    mergedAt
                    createdAt
                    updatedAt
                    closedAt
                    state
                    bodyText
                }
            }
            pageInfo {
                endCursor
                hasNextPage
            }
        }
    }
}
"""

COMMITS = """
query Commits($owner: String!, $name: String!, $n: Int, $cursor: String) {
    repository(owner: $owner, name: $name) {
        id
        name
        url
        defaultBranchRef {
            target {
                ... on Commit {
                    history(first: $n, after: $cursor) {
                        edges {
                            node {
                                id
                                committedDate
                                pushedDate
                                message
                                author {
                                    name
                                }
                            }
                        }
                        pageInfo {
                            endCursor
                            hasNextPage
                        }
                    }
                }
            }
        }
    }
}
"""

STARS = """
query Stars($owner: String!, $name: String!, $n: Int, $cursor: String) {
    repository(owner: $owner, name: $name) {
        id
        name
        url
        stargazers(first: $n, after: $cursor) {
            edges {
                starredAt
                node {
                    login
                    company
                }
            }
            pageInfo {
                endCursor
                hasNextPage
            }
        }
    }
}
"""

FORKS = """
query Forks($owner: String!, $name: String!, $n: Int, $cursor: String) {
    repository(owner: $owner, name: $name) {
        id
        name
        url
        forks(first: $n, after: $cursor) {
            edges {
                node {
                    createdAt
                    owner {
                        ... on User {
                            login
                            company
                        }
                    }
                }
            }
            pageInfo {
                endCursor
                hasNextPage
            }
        }
    }
}
"""

WATCHERS = """
query Watchers($owner: String!, $name: String!, $n: Int, $cursor: String){
    repository(owner: $owner, name: $name) {
        id
        name
        url
        watchers(first: $n, after: $cursor) {
            edges {
                node {
                    createdAt
                    company
                    login
                }
            }
            pageInfo {
                endCursor
                hasNextPage
            }
        }
    }
}
"""