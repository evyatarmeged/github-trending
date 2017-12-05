# Pytrend-CLI
#### A command line tool for fetching GitHub trending repositories.

### Description
Pytrend-CLI is a command line tool for getting the latest (actually, current, per call) information 
about trending repositories/developers on GitHub.<br>
Pytrend can be filtered by programming language or trending period (daily/weekly/monthly).<br>
Currently supports top 15 most popular programming languages on GitHub (by open PRs) plus HTML.
![langs](http://oi64.tinypic.com/v2wp.jpg)

All data is taken from <a href='https://octoverse.github.com/'>GitHub octoverse</a>.


### Installation
pip install pytrend-cli


### Usage
Just call `pytrend` from the command line followed by (optional) wanted arguments.<br>
Using the `--dev` flag will show information about trending developers instead of repositories. This flag can also be
filtered with `--weekly` or `--monthly` flags, or a specified language.<br>
An argument free call to `pytrend` will result in the top 25 *repositories* from *all* languages trending *daily*.<br>

### Options/Flags
```
optional arguments:
  -h, --help           show this help message and exit
  --language LANGUAGE  Programming language to display repositories for
  --dev                  Get trending developers instead of repositories
  --weekly             Display trending repositories from the past week
  --monthly           Display trending repositories from the past month
  --json                 Save data to a JSON file
```

