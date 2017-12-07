import logging

BASE_URL = 'https://github.com/'
TRENDING_URL = BASE_URL + 'trending/'
ACCEPTED_LANGUAGES = ['javascript', 'python', 'java', 'ruby', 'php', 'c++', 'css', 'c#',
                      'go', 'c', 'typescript', 'shell', 'swift', 'scala', 'objective-c', 'html']
logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.INFO)
LOGGER = logging.getLogger()
XML_DECLARATION = '<?xml version="1.0" encoding="UTF-8" ?>\n'
RECORD = '\t<record>\n'
END_RECORD = '\t</record>\n'
ITEM = '\t\t<{0}>{1}</{0}>\n'
ROOT = '<root>\n'
END_ROOT = '</root>'
