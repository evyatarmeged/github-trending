import logging
import click
from datetime import datetime
import json as JSON  # Importing as caps to enable @click argument `json`
import requests
from bs4 import BeautifulSoup

# Constants

BASE_URL = 'https://github.com/'
TRENDING_URL = BASE_URL + 'trending/'
ACCEPTED_LANGUAGES = [
    'javascript', 'python', 'java', 'ruby', 'php', 'c++', 'css', 'c#', 'go',
    'c', 'typescript', 'shell', 'swift', 'scala', 'objective-c', 'html',
    'rust', 'coffeescript', 'haskell', 'groovy', 'lua', 'elixir',
    'perl', 'kotlin', 'clojure'
]
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)
LOGGER = logging.getLogger()
XML_DECLARATION = '<?xml version="1.0" encoding="UTF-8" ?>\n'
RECORD = '\t<record>\n'
END_RECORD = '\t</record>\n'
ITEM = '\t\t<{0}>{1}</{0}>\n'
ROOT = '<root>\n'
END_ROOT = '</root>'

# Repository information parsing functions


def username_and_reponame(repo_info):
    """Return user name and repository name"""
    try:
        data = repo_info.find('a').get('href').split('/')
        try:
            username = data[1]
        except IndexError:
            username = None
        try:
            repo_name = data[2]
        except IndexError:
            repo_name = None
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
        # Handle no stars/pull requests data on repo
        try:
            stars = data[0].text.strip()
        except IndexError:
            stars = None
        try:
            pull_requests = data[1].text.strip()
        except IndexError:
            pull_requests = None
        return stars, pull_requests
    except AttributeError:
        return


def get_stars_trending(repo_info):
    """Return stars trending"""
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
                'Stars trending': get_stars_trending(list_item)
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
    """Establish connection with url"""
    page = requests.get(url)
    if page.status_code != 200:
        if page.status_code == 429:
            LOGGER.error('Too many requests')
        else:
            LOGGER.error('Could not establish connection with GitHub')
        exit(1)
    return page


def add_duration_query(url, weekly=None, monthly=None):
    """Add duration according to arguments"""
    if weekly:
        url += '?since=weekly'
    elif monthly:
        url += '?since=monthly'
    return url


def write_json(data):
    with open(str(datetime.now()) + '.json', 'w') as file:
        file.write(JSON.dumps(data, indent=4))


def write_xml(data):
    """Write XML file """
    xml = XML_DECLARATION + ROOT
    for info in data.values():
        xml += RECORD
        for key, value in info.items():
            try:
                xml += ITEM.format(''.join(key.split()),
                                   value.encode('ascii',
                                                'ignore').decode('utf8'))
            except AttributeError:
                pass
        xml += END_RECORD
    xml += END_ROOT
    with open(str(datetime.now()) + '.xml', 'w') as file:
        file.write(xml)


def build_url(language=None, dev=False, monthly=False, weekly=False):
    """Build destination URL according to arguments"""
    url = TRENDING_URL
    if dev:
        url += '/developers/'
    if language:
        if language.lower() == 'c#':
            url += 'c%23'  # Handle C# url encoding
        else:
            url += language.lower()
    url = add_duration_query(url=url, weekly=weekly, monthly=monthly)
    return url


def get_metadata(language, dev, monthly, weekly):
    """Build URL, connect to page and create BeautifulSoup object, build and return result"""
    url = build_url(language=language, dev=dev, monthly=monthly, weekly=weekly)
    page = make_connection(url)
    soup = BeautifulSoup(page.text, 'lxml')
    explore_content = soup.select('.explore-content')
    if dev:
        result = parse_developers_info(explore_content)
    else:
        result = parse_repositories_info(explore_content)
    return result


@click.command()
@click.option('--language', '-l', help='Display repositories for this programming language')
@click.option('--dev', '-d', is_flag=True, help='Get trending developers instead of repositories')
@click.option('--weekly', '-w', is_flag=True, help='Display trending repositories from the past week')
@click.option('--monthly', '-m', is_flag=True, help='Display trending repositories from the past month')
@click.option('--json', '-j', is_flag=True, help='Save data to a JSON file')
@click.option('--xml', '-x', is_flag=True, help='Save data to an XML file')
@click.option('--silent', '-s', is_flag=True, help='Do not write to sdout')
def main(language, dev, weekly, monthly, json, xml, silent):
    """
    Parse arguments using click, check for argument validation and call get_metadata function.
    Either print or write results to JSON/XML
    """
    if language and language.lower() not in ACCEPTED_LANGUAGES:
        LOGGER.error(
            'Specified programming language not in supported languages')
        exit(1)
    if weekly and monthly:
        LOGGER.error('Please specify weekly OR monthly')
        exit(1)
    if silent and not json and not xml:
        LOGGER.error('Passed silent flag without JSON or XML flags. exiting')
        exit(1)
    result = get_metadata(
        language=language, dev=dev, monthly=monthly, weekly=weekly)
    if not silent:
        print(JSON.dumps(result, indent=4))
    if json:
        write_json(result)
    if xml:
        write_xml(result)
