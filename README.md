# courseutils
helper code for class

## To install:

```
git clone https://github.com/introcompsys/courseutils
cd courseutils
pip install .
```

You may need to use pip3 instead of pip.
On Windows, use GitBash for the clone and then Anaconda Prompt for install

## To upgrade:
```
cd courseutils
git pull
pip install .
```


You may need to use pip3 instead of pip
On Windows, use GitBash for the clone and then Anaconda Prompt for install
## Usage

This is a command line tool. It works in Bash on MacOS and Linux and Anaconda Prompt on Windows.

### Get tasks to do

Get prepare for the most recent date (what's current)
```
sysgetassignment
```

Or give it the date and level

```
sysgetassignment --date 2022-10-19 --type review
```

### Get the list for use in a bash script (sp22 only)

use `kwlfilecheck` to get the list of files from that should be in the kwl repo.

Usage: kwlfilecheck [OPTIONS]

  scrape the list, filter and echo back

Options:
-  `--practice`   flag formore practice related files or not
-  `--zone TEXT`
-  `--help`       Show this message and exit.


### File Counter by date

use `kwlfilecount` to check the dates that are/not complete and the count

Usage: kwlfilecount [OPTIONS]

Options:
- `--practice`   flag formore practice related files or not
-  `--zone TEXT`
-  `--help`       Show this message and exit.
