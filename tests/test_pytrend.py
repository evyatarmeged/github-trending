import os
import unittest
import json
from random import choice
from click.testing import CliRunner
from pytrend_cli.pytrend import *
import uuid


class PyTrendTestCase(unittest.TestCase):
    """Unittests"""

    def setUp(self):
        self.runner = CliRunner()
        self.base_url = 'https://github.com/'
        self.trending_url = self.base_url + 'trending/'
        self.weekly = '?since=weekly'
        self.monthly = '?since=monthly'
        self.languages = ['javascript', 'python', 'java', 'ruby', 'php', 'c++', 'css', 'c#',
                          'go', 'c', 'typescript', 'shell', 'swift', 'scala', 'objective-c', 'html']
        self.page = make_connection(self.trending_url)
        self.mock_data = BeautifulSoup(self.page.text, 'lxml').select('.explore-content')

    def test_weekly_and_monthly_error(self):
        result = self.runner.invoke(main, ['-m', '-w'])
        self.assertNotEqual(result.exit_code, 0)

    def test_silent_no_output(self):
        result = self.runner.invoke(main, ['-s'])
        self.assertNotEqual(result.exit_code, 0)

    def test_build_url_no_args(self):
        url = build_url()
        self.assertEqual(url, self.trending_url)

    def test_build_url_lang(self):
        random_string = uuid.uuid4().hex
        url = build_url(language=random_string)
        self.assertEqual(url, self.trending_url + random_string)

    def test_build_url_lang_c_sharp(self):
        url = build_url(language='c#')
        self.assertEqual(url, self.trending_url + 'c%23')

    def test_build_url_caps(self):
        random_string = uuid.uuid4().hex
        url = build_url(language=random_string.upper())
        self.assertEqual(url, self.trending_url + random_string.lower())

    def test_duration_query_no_args(self):
        url = add_duration_query(url=self.trending_url)
        self.assertEqual(url, self.trending_url)

    def test_duration_query_weekly(self):
        url = add_duration_query(self.trending_url, weekly=self.weekly)
        self.assertEqual(url, self.trending_url + self.weekly)

    def test_duration_query_monthly(self):
        url = add_duration_query(self.trending_url, monthly=self.monthly)
        self.assertEqual(url, self.trending_url + self.monthly)

    # Request & I/O testing

    def test_connection(self):
        self.assertEqual(200, make_connection(self.trending_url).status_code)

    def test_lang(self):
        # Invoke main() for each supported languages (github can take it)
        for language in self.languages:
            result = self.runner.invoke(main, ['-l', language])
            repos = json.loads(result.output)
            for key in repos.keys():
                self.assertEqual(repos.get(key).get('Programming Language').lower(), language)

    def test_no_output_on_silent(self):
        flags = ['-j', '-x']
        result = self.runner.invoke(main, [choice(flags), '-s'])
        self.assertFalse(result.output)
        for _, __, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith('.xml') or file.endswith('.json'):
                    os.remove(file)

    def test_xml_writing(self):
        write_xml(parse_repositories_info(self.mock_data))
        exists = False
        xml_file = None
        for _, __, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith('.xml'):
                    xml_file = file
                    exists = True
        self.assertTrue(exists)
        if xml_file:
            os.remove(xml_file)

    def test_json_writing(self):
        write_json(parse_repositories_info(self.mock_data))
        exists = False
        json_file = None
        for _, folders, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith('.json'):
                    json_file = file
                    exists = True
        self.assertTrue(exists)
        if json_file:
            os.remove(json_file)
