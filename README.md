# Loadshedding

A simple yet clean script that displays loadshedding schedule.

## Usage

```bash
loadshedding [-h] [-f] -g N [-e | -r | -m]

optional arguments:
  -h, --help       show this help message and exit
  -f, --force      force update
  -g N, --group N  force schedule update
  -e, --effective  show effective time
  -r, --relative   show remaining time
  -m, --more       show all time
```

## Example

Show time left for group 2

    $ ./loadshedding.py --group 2 --relative
    4h40m N

Show loadshedding schedule for group 2

    $ ./loadshedding.py --group 2 --more
    1	04:00-11:00	15:00-21:00
    2	05:00-14:00	18:00-22:00
    3*	11:00-19:00
    4	03:00-10:00	14:00-20:00
    5	06:00-15:00	19:00-23:00
    6	10:00-16:00	20:00-23:59
    7	04:00-12:00	16:00-22:00

## Getting Started

Checkout the latest sources:

    git clone https://github.com/tnagorra/loadshedding

Get the dependencies:

    pip install requests beautifulsoup4

Simply run the script or copy the script in /usr/local/bin.
