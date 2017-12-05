import json
import argparse
from datetime import datetime
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from pytrend_cli.constants import TRENDING_URL, ACCEPTED_LANGUAGES, BASE_URL, LOGGER


# Repository information parsing functions

def username_and_reponame(repo_info):
    """Return user name and repository name"""
    try:
        _, username, repo_name = repo_info.find('a').get('href').split('/')
        return username, repo_name
    except AttributeError:
        return


def get_description(repo_info):
    """Return repository description"""
    try:
        return repo_info.find('p').text.strip()
    except AttributeError:
        return


def get_programming_language(repo_info):
    """Return programming language used for repository"""
    try:
        return repo_info.find('span', {'itemprop': 'programmingLanguage'}).text.strip()
    except AttributeError:
        return


def stars_and_pull_requests(repo_info):
    """Return total stars and pull requests"""
    try:
        data = repo_info.select('a.muted-link')
        stars = data[0].text.strip()
        pull_requests = data[1].text.strip()
        return stars, pull_requests
    except AttributeError:
        return


def get_stars_today(repo_info):
    """Return stars gained today"""
    try:
        return repo_info.find('span', {'class': 'float-sm-right'}).text.strip()
    except AttributeError:
        return


def parse_repositories_info(tag):
    """
    Scrape trending repository info
    :return A dictionary of all trending repositories filtered by arguments from user
    """
    trending = {}
    for content in tag:
        repositories = content.find_all('li')
        for index, list_item in enumerate(repositories, start=1):
            username, repo_name = username_and_reponame(list_item)
            stars, pull_requests = stars_and_pull_requests(list_item)
            trending[index] = {
                'User': username,
                'Repository': repo_name,
                'URL': BASE_URL + '/'.join((username, repo_name)),
                'Description': get_description(list_item),
                'Programming Language': get_programming_language(list_item),
                'Total stars': stars,
                'Pull requests': pull_requests,
                'Stars Trending': get_stars_today(list_item)
            }
    return trending

# END Repository parsing functions


# Developer information parsing functions

def get_developer(repo_info):
    """Get trending developer name"""
    try:
        developer = ' '.join(repo_info.find('h2').find('a').text.split())
        return developer
    except AttributeError:
        return


def get_profile(repo_info):
    """Get trending developer profile url"""
    try:
        profile = BASE_URL + repo_info.find('h2').find('a').get('href')
        return profile
    except AttributeError:
        return


def get_developer_repo(item):
    """
    Get the repository that made the developer trending
    :return repository name and url
    """
    try:
        a = item.find('a', {'class': 'repo-snipit'})
        url = BASE_URL + a.get('href').strip()
        repo_name = a.find('span').text.strip()
        return repo_name, url
    except AttributeError:
        return


def parse_developers_info(tag):
    """
    Scrape trending developer info
    :return A dictionary with all trending developers filtered by arguments from user
    """
    trending = {}
    for content in tag:
        repositories = content.find_all('li')
        for index, list_item in enumerate(repositories, start=1):
            repo_name, url = get_developer_repo(list_item)
            trending[index] = {
                'Developer': get_developer(list_item),
                'Profile': get_profile(list_item),
                'Repository': repo_name,
                'URL': url
            }
    return trending

# END Developer parsing functions


# All around functions

def make_connection(url):
    page = requests.get(url)
    if page.status_code != 200:
        if page.status_code == 429:
            LOGGER.error('Too many requests')
        else:
            LOGGER.error('Could not establish connection with GitHub')
        return
    return page


def add_duration_query(url):
    if ARGS.get('weekly'):
        return url + '?since=weekly'
    elif ARGS.get('monthly'):
        return url + '?since=monthly'
    return url


def get_metadata(dev=False):
    url = TRENDING_URL
    if dev:
        url += '/developers/'
    if ARGS.get('language'):
        if ARGS.get('language').lower() == 'c#':
            url += 'c%23'  # Handle C# url encoding
        else:
            url += ARGS.get('language').lower()
    url = add_duration_query(url)
    page = make_connection(url)
    soup = BeautifulSoup(page.text, 'lxml')
    explore_content = soup.select('.explore-content')
    if dev:
        return parse_developers_info(explore_content)
    return parse_repositories_info(explore_content)


def main():
    if ARGS.get('language') and ARGS.get('language').lower() not in ACCEPTED_LANGUAGES:
        LOGGER.error('Specified programming language not in supported languages')
        return
    if ARGS.get('weekly') & ARGS.get('monthly'):
        LOGGER.error('Please specify weekly OR monthly')
        return
    result = get_metadata(dev=ARGS.get('dev'))
    if not ARGS.get('silent'):
        pprint(result)
    if ARGS['json']:
        with open(str(datetime.now()) + '.json', 'w+') as file:
            file.write(json.dumps(result, indent=4, sort_keys=True))


def entry_point():
    """Function to use for setup.py as a console script entry point"""
    parser = argparse.ArgumentParser('Get trending GitHub repositories daily/weekly/monthly and by language')
    parser.add_argument('--language', help='Display repositories for this programming language')
    parser.add_argument('--dev', action='store_true', help='Get trending developers instead of repositories')
    parser.add_argument('--weekly', action='store_true', help='Display trending repositories from the past week')
    parser.add_argument('--monthly', action='store_true', help='Display trending repositories from the past month')
    parser.add_argument('--json', action='store_true', help='Save data to a JSON file')
    parser.add_argument('--silent', action='store_true', help='Do not write to sdout')
    global ARGS
    ARGS = vars(parser.parse_args())
    main()
