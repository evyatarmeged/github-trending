# Pytrend-CLI
#### A command line tool for fetching GitHub trending repositories.

[![Build Status](https://travis-ci.org/evyatarmeged/github-trending.svg?branch=master)](https://travis-ci.org/evyatarmeged/github-trending)
[![PyPI version](https://badge.fury.io/py/pytrend-cli.svg)](https://badge.fury.io/py/pytrend-cli)
[![pyversion](https://img.shields.io/badge/python-2.7%2C%203.5-blue.svg?style=plastic)]()
[![downloads](https://img.shields.io/badge/downloads-1.5k-lightgrey.svg)]()
[![license](https://img.shields.io/badge/license-MIT-blue.svg)]()
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/8db8f9940d1d4994a2cd217e5096dce8)](https://www.codacy.com/app/evyatarmeged/github-trending?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=evyatarmeged/github-trending&amp;utm_campaign=Badge_Grade)

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

