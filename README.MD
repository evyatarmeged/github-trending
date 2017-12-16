# Pytrend-CLI
#### A command line tool for fetching GitHub trending repositories.

[![Scrutinizer Build](https://img.shields.io/scrutinizer/build/g/filp/whoops.svg?style=plastic)]()
[![version](https://img.shields.io/badge/version-1.17-brightgreen.svg?style=plastic)]()
[![pyversion](https://img.shields.io/badge/python-2.7%2C%203.5-blue.svg?style=plastic)]()
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=plastic)]()

### Description
Pytrend-CLI is a command line tool for getting the latest (actually, current, per call) information 
about trending repositories/developers on GitHub.<br>
Pytrend can be filtered by programming language or trending period (daily/weekly/monthly).<br>
Currently supports top 15 most popular programming languages on GitHub (by open PRs) plus HTML.
![langs](http://oi64.tinypic.com/v2wp.jpg)

All data is taken from <a href='https://octoverse.github.com/'>GitHub octoverse</a>.


### Installation
`pip install pytrend-cli`


### Usage
Call `pytrend` from the command line followed by (optional) arguments.<br>
Using the `--dev` flag will show information about trending developers instead of repositories. This flag can also be
filtered with `--weekly` or `--monthly` flags, or a specified language.<br>
An argument free call to `pytrend` will result in the top 25 *repositories* from *all* languages trending *daily*.<br>

### Options/Flags
```
Usage: pytrend [OPTIONS]

Options:
  -l, --language TEXT  Display repositories for this programming language
  -d, --dev            Get trending developers instead of repositories
  -w, --weekly         Display trending repositories from the past week
  -m, --monthly        Display trending repositories from the past month
  -j, --json           Save data to a JSON file
  -x, --xml            Save data to an XML file
  -s, --silent         Do not write to sdout
  --help               Show this message and exit.
```

