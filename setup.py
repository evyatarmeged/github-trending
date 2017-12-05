from setuptools import setup

setup(
    name='pytrend-cli',
    packages=['pytrend-cli'],
    license='MIT',
    version='1.0',
    description='Get trending GitHub repositories daily/weekly/monthly and by language',
    author='Evyatar Meged',
    author_email='evyatarmeged@gmail.com',
    url='https://github.com/evyatarmeged/pytrend-cli',
    keywords=['GitHub', 'trending', 'repositories', 'developers', 'scraping'],
    classifiers=['Programming Language :: Python :: 3'],
    install_requires=['beautifulsoup4>=4.4.1', 'requests>=2.18.4'],
    entry_points={
        'console_scripts': [
            'pytrend = pytrend_cli.pytrend'
        ]
    },
)
