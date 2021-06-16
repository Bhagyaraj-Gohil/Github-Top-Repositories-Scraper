from HelperFunctions import *
import pandas as pd

base_url = 'http://github.com'
github_topics_pagewise = [
    "https://github.com/topics?page=1",
    "https://github.com/topics?page=2",
    "https://github.com/topics?page=3",
    "https://github.com/topics?page=4",
    "https://github.com/topics?page=5",
    "https://github.com/topics?page=6",
    "https://github.com/topics?page=7"
]

#result will be stored in the following dictionary
result = {
    'username': [],
    'repository_name' : [],
    'stars' : [],
    'forks' : [],
    'issues' : [],
    'pull_requests' : [],
    'topic' : [],
    'repository_url' : []
}

for page in github_topics_pagewise:
   scrape_main_page(page, result)

top_repos_df = pd.DataFrame(result)
top_repos_df.to_csv('Top Repositories.csv', index = None)