import requests
from bs4 import BeautifulSoup

#following class names will be used to get required elements
base_url = 'http://github.com'
topic_name_class = 'f3 lh-condensed mb-0 mt-1 Link--primary'
topic_url_class = 'd-flex no-underline'
repo_name_and_desc_class = 'f3 color-text-secondary text-normal lh-condensed'
repo_stars_and_forks_class = 'social-count'
repo_counts_class = 'Counter'

def parse_int_title(s):
    s.strip()
    s = s.replace(',','')
    s = s.replace('+','')
    return int(s)

def parse_int_aria_label(s):
    return int(s.split(' ')[0])

def get_urls(base_url, a_tags):
    result = []
    for tag in a_tags:
        result.append(base_url + tag['href'])
    return result

def get_text(tags):
    result = []
    for tag in tags:
        result.append(tag.text.strip())
    return result

#Function that gets details about individual repository
def get_repo_details(repo_url):
    response = requests.get(repo_url)
    
    #error handling
    if response.status_code != 200:
        raise Exception("Failed to load " + url)
        
    doc = BeautifulSoup(response.text, 'html.parser')
    
    #Getting number of stars and forks
    star_tag, fork_tag = doc.find_all(class_= repo_stars_and_forks_class)
    stars = parse_int_aria_label(star_tag['aria-label'])
    forks = parse_int_aria_label(fork_tag['aria-label'])
    
    #Getting number of issues and pull_requests
    span_tags_raw = doc.find_all('span', {'class' : repo_counts_class, 'data-view-component' : 'true'})
    span_tags_raw = doc.find_all('span', {'class' : repo_counts_class, 'data-view-component' : 'true'})
    span_tags_na = doc.find_all('span', {'class' : repo_counts_class, 'data-view-component' : 'true','title' : 'Not available'})
    span_tags = []
    for tag in span_tags_raw:
        if tag.has_attr('hidden') or tag in span_tags_na:
            continue
        span_tags.append(tag)
        
    issues = parse_int_title(span_tags[0]['title']) if 1 <= len(span_tags) else 0
    pull_requests = parse_int_title(span_tags[1]['title']) if 2 <= len(span_tags) else 0
    
    return stars, forks, issues, pull_requests


#gets repo_name, username and repo_url
def get_repo_info(tags, topic_name, result):
    for tag in tags:
        result['topic'].append(topic_name)
        username_tag, repo_name_tag = tag.findChildren('a', recursive=False)
        username = username_tag.text.strip()
        repo_name = repo_name_tag.text.strip()
        repo_url = base_url + repo_name_tag['href']
        result['username'].append(username)
        result['repository_name'].append(repo_name)
        result['repository_url'].append(repo_url)
        
        #call get_repo_details()
        stars, forks, issues, pull_requests = get_repo_details(repo_url)
        result['stars'].append(stars)
        result['forks'].append(forks)
        result['issues'].append(issues)
        result['pull_requests'].append(pull_requests)


#gets information from the specified topic page
def scrape_topic_page(topic, url, result):
    print(f'Scraping top repositories for "{topic}"')
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to load " + url)
    
    doc = BeautifulSoup(response.text, 'html.parser')
    repo_name_tags = doc.find_all(class_ = repo_name_and_desc_class)
    get_repo_info(repo_name_tags, topic, result)


#scrapes the main page (Eg : "http://github.com/topics?page=1")
def scrape_main_page(url, result):
    print("Scraping list of topics from " + url)
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to load " + url)
    
    doc = BeautifulSoup(response.text, 'html.parser')
    
    #getting topic information
    topic_name_tags = doc.find_all('p', {'class' : topic_name_class})
    topic_url_tags = doc.find_all('a', {'class' : topic_url_class})
    topic_names = get_text(topic_name_tags)
    topic_urls = get_urls(base_url, topic_url_tags)
    
    for i in range(len(topic_urls)):
        scrape_topic_page(topic_names[i], topic_urls[i], result)