#!/usr/bin/env python3

import os, sys, json, argparse, re, time, datetime
import requests
from bs4 import BeautifulSoup

class ConnectError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

""" Scrap the routine from certain url """
def _scrapRoutine():
    # Get content from the url
    url = 'http://battigayo.com/schedule'
    try:
        response = requests.get(url)
    except:
        raise ConnectError("ERROR Connection Problem")

    if response.status_code != 200:
        raise ConnectError("ERROR code: "+str(response.status_code))
    # Regex to match time
    timerange = re.compile(r"[0-9]{1,2}:[0-9]{2}-[0-9]{2}:[0-9]{2}")
    # Get a parser for html
    extractor = BeautifulSoup(response.content, "html.parser")
    # Iterate over tr and td

    routines = []
    for daywise in extractor.find_all('li', class_="clearfix" )[1:]:
        routine = []
        for hourwise in daywise.find_all('div'):
            time_list = [[[int(y) for y in z.split(':')]
                for z in x.split('-')]
                for x in timerange.findall(hourwise.get_text())]
            if time_list:
                routine.append(time_list)
        routines.append(routine)

    # In cases where a response is given but not essentially the routine page
    # Ex: Subisu login page
    if not routines:
        raise ConnectError("ERROR Couldn't scrap routine")

    return routines

""" Load the routine from file or scrap from the url """
def loadRoutine(force, freq=1):

    """ Find out how old the file is """
    def _age(fyle):
        created = os.path.getctime(fyle)
        today = time.time()
        return (today-created)/(60*60*24) #in days

    dest = os.path.expanduser("~")
    fname = dest+'/.loadshedding.routine'
    if os.path.exists(fname) and _age(fname) <= 2 and not force:
        with open(fname) as datafile:
            routines = json.load(datafile)
    else:
        try:
            routines = _scrapRoutine()
            with open(fname, 'w') as outfile:
                json.dump(routines, outfile)

        except ConnectError as e:
            if not os.path.exists(fname):
                print(e)
                exit(1)
            # print('*', end='')
            with open(fname, 'r') as datafile:
                routines = json.load(datafile)
    return routines


""" Show the status for 'relative' and 'absolute' option """
def status(routines, group, relative):

    """ _prettify output for 'relative' option """
    def _prettify(tym):
        time = int(tym.total_seconds())
        tuples = [('s',60), ('m', 60), ('h', 24),
                  ('d', 365), ('y', 9999)]
        output = []
        for t in tuples:
            tmp = time % t[1]
            if tmp:
                output.insert(0, str(tmp)+t[0])
            time //= t[1]
        # Get first two elements only
        op = ''.join(output[0:min(len(output), 2)])
        if not op:
            op = '0s'
        return op

    """ _prettify output for 'absolute' option """
    def _prettify2(tym):
        return tym.strftime("%H:%M")

    def _sanitize(rng):
        if rng[0]==24:
            return {"hour":23, "minute":59, "second":59}
        else:
            return {"hour":rng[0], "minute":rng[1], "second":0}

    # current time
    now = datetime.datetime.now()

    # now = datetime.datetime(2016, 4, 28, 20, 51)

    week = now.isoweekday()%7+1
    routine = routines[group-1][week-1]
    for rng in routine:
        start = now.replace(**_sanitize(rng[0]))
        end = now.replace(**_sanitize(rng[1]))
        # If end is smaller than start, then it is in another day
        if end < start:
            end += datetime.timedelta(days=1)

        if now < start:
            z = _prettify(start-now) if relative else _prettify2(start)
            return z+" Y"
        elif now >= start and now <= end:
            z = _prettify(end-now) if relative else _prettify2(end)
            return z+" N"
        # what do we do here?
    else:
        # Iterate over the week
        x = 0
        while x < 7:
            x += 1
            week = (week+x-1)%7 + 1
            routine = routines[group-1][week-1]
            if not routine:
                continue
            rng = routine[0]

            start = now.replace(**_sanitize(rng[0]))
            start += datetime.timedelta(days=1)

            # in prettify2, x represents the time after certain days
            z = _prettify(start-now) if relative else (_prettify2(start)
                                                       +" "+str(x))
            return z+" Y"
        return "Never"+" Y"

""" Show the status for 'schedule' option """
def statusSchedule(routines, group):
    now = datetime.datetime.now()
    routine = routines[group-1]
    week = now.isoweekday()%7+1

    op = ''
    for i, day in enumerate(routine):
        op += str(i+1) if (i+1)!=week else '*'
        op += ' '
        for rng in day:
            op += '{:02d}:{:02d}'.format(rng[0][0], rng[0][1])
            op += '-'
            op += '{:02d}:{:02d}'.format(rng[1][0], rng[1][1])
            op += ' '
        op += '\n'
    # remove last new line
    op = op[:-1]
    return op


def parse():
    parser = argparse.ArgumentParser("loadshedding", description=
                                     "Display loadshedding schedule.")
    parser.add_argument('-f', '--force', dest='force', help='force update',
                        action='store_const', const=True)
    parser.add_argument('-g', '--group',  dest='group', metavar='N',
                        help='force schedule update', type=int, required=True)

    optype = parser.add_mutually_exclusive_group(required=False)
    optype.add_argument('-a', '--absolute', dest='relative',
                        help='show absolute time',
                        action='store_const', const=False)
    optype.add_argument('-r', '--relative', dest='relative',
                        help='show remaining time',
                        action='store_const', const=True)
    optype.add_argument('-s', '--schedule', dest='schedule',
                        help='show time schedule',
                        action='store_const', const=True)

    return parser.parse_args()

def main():
    args = parse()
    routines = loadRoutine(args.force)

    if args.group < 1 or args.group > len(routines):
        print("ERROR Group value out of bounds.")
        exit(1)
    if args.schedule:
        op = statusSchedule(routines, args.group)
    else:
        op = status(routines, args.group, args.relative)

    print(op)
    return 0

if __name__=="__main__":
    main()
