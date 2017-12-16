import unittest
from click.testing import CliRunner
from pytrend_cli.pytrend import *
import uuid


class PyTrendTestCase(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        self.base_url = 'https://github.com/'
        self.trending_url = self.base_url + 'trending/'
        self.weekly = '?since=weekly'
        self.monthly = '?since=monthly'

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

