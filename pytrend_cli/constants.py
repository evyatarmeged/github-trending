import logging

BASE_URL = 'https://github.com/'
TRENDING_URL = BASE_URL + 'trending/'
ACCEPTED_LANGUAGES = ['javascript', 'python', 'java', 'ruby', 'php', 'c++', 'css', 'c#',
                      'go', 'c', 'typescript', 'shell', 'swift', 'scala', 'objective-c', 'html']
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)
LOGGER = logging.getLogger()