# Loadshedding

A simple and clean script that displays loadshedding schedule.

## Usage

```bash
usage: loadshedding [-h] [-f] -g N [-a | -r | -s]

Display loadshedding schedule.

optional arguments:
  -h, --help       show this help message and exit
  -f, --force      force update
  -g N, --group N  force schedule update
  -a, --absolute   show absolute time
  -r, --relative   show remaining time
  -s, --schedule   show time schedule
```

## Example

Show time left for group 2

```bash
$ loadshedding --group 2 --relative
4h40m N
```

Show loadshedding schedule for group 2

```bash
$ loadshedding --group 2 --schedule
* 04:00-10:00 14:00-19:00 
2 06:00-14:00 17:00-21:00 
3 10:00-17:00 20:00-23:00 
4 09:00-16:00 19:00-22:30 
5 05:00-12:00 16:00-20:00 
6 07:00-15:00 18:00-21:30 
7 04:00-09:00 12:00-18:00 
```

## Getting Started

Checkout the latest sources:

    git clone https://github.com/tnagorra/loadshedding

Get the dependencies:

    pip install requests beautifulsoup4

Simply run the install.sh script or copy the script in /usr/local/bin.
