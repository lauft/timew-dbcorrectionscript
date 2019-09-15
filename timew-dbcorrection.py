#!/usr/bin/env python

from __future__ import print_function

import json
import os
import subprocess
import sys

try:
    input = raw_input
except NameError:
    pass


def get_version():
    timew_binary = os.getenv("TIMEW_BIN", "timew")
    return subprocess.check_output([timew_binary, "--version"]).decode("UTF-8").strip()


def draw_progress_bar(percent, bar_length=20):
    sys.stdout.write("\r")
    progress = ""
    for i in range(bar_length):
        if i < int(bar_length * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()


if __name__ == "__main__":
    # check version
    version_string = get_version()
    version_array = version_string.split(".")
    major_version = int(version_array[0])
    minor_version = int(version_array[1])
    patch_version = int(version_array[2])

    if major_version <= 1 and minor_version <= 1 and patch_version < 1:
        print("This script requires TimeWarrior version 1.1.1 or larger!")
        exit(1)

    # show disclaimer
    print("""
TIMEWARRIOR DATABASE CORRECTION SCRIPT

Use this script when you have used
 - TimeWarrior earlier than version 1.1.1
 - Exclusions

If none of the above applies, you probably do not need to run this script.

The script will only correct the database for ONE set of exclusions. If you
have changed your exclusions only the current state will be restored!

This script will export your stored intervals, purge your database and re-enter
your data such that exclusions will be applied and written properly to the
database.

For further information on this see 
https://taskwarrior.org/docs/timewarrior/dbcorrection.html

!!! YOU ARE STRONGLY ADVISED TO BACKUP YOUR DATABASE BEFORE PROCEEDING !!!

""")

    # first chance to bail out
    answer = input("Proceed? [y/N] ")

    if answer != "y" and answer != "Y":
        print("Exiting script")
        exit(0)

    # gather data and print diagnostics
    print("Gathering information...")

    timew_binary = os.getenv("TIMEW_BIN", "timew")
    database_path = os.getenv("TIMEWARRIORDB", os.path.expanduser("~/.timewarrior"))

    files = os.listdir(os.path.join(database_path, "data"))

    export_data_file = os.getenv("TIMEW_EXPORT_DATA", None)

    print("TimeWarrior binary: '%s'" % timew_binary)
    print("TimeWarrior version: '%s'" % version_string)
    print("Database path: '%s'" % database_path)
    print("(you can change this by setting environment variable TIMEWARRIORDB)")
    print("Found files: %s" % ", ".join(files))

    if export_data_file is not None:
        print("Supplied data file: {}".format(export_data_file))

    print("")
    print("The script will now extract your data, purge your database, and re-enter your intervals.")

    # last chance to bail out
    answer = input("Proceed? [y/N] ")

    if answer != "y" and answer != "Y":
        print("Exiting script")
        exit(0)

    if export_data_file is None:
        # export database
        print("Exporting database...")
        data = subprocess.check_output([timew_binary, "export"]).decode("UTF-8").strip()
    else:
        # load data from supplied file
        print("Loading data from '{}'".format(export_data_file))
        with open(export_data_file) as f:
            data = f.read().strip()

    try:
        # extract intervals
        intervals = json.loads(data)
    except Exception as e:
        print("")
        print("Something went wrong while importing your data:")
        print("")
        print(e)
        print("""
Try to export your data into a file (e.g. `timew export > data.json`) and check
the JSON data. (The error message above might give you a hint on which line to
look at.)

When you have fixed your data, rerun this script providing the corrected JSON
via the environment variable `TIMEW_EXPORT_DATA`:

    $ TIMEW_EXPORT_DATA=path/to/data.json ./timew-dbcorrection.py
""")
        exit(1)

    interval_count = len(intervals)
    print("Extracted %d interval(s)" % interval_count)

    # purge database
    print("Purging database (" + os.path.join(database_path, "data") + ")...")

    for file in files:
        sys.stdout.write("Deleting %s" % file)
        sys.stdout.write("\r")
        sys.stdout.flush()
        os.remove(os.path.join(database_path, "data", file))

    # import database
    print("Re-importing database...")
    print("(This may take some time, please be patient)")
    counter = 0

    for interval in intervals:
        counter += 1
        ratio = float(counter)/interval_count
        draw_progress_bar(ratio, 20)

        if "start" in interval:
            if 'tags' in interval:
                subprocess.check_output([timew_binary, "start", interval["start"]] + interval['tags']).decode("UTF-8")
            else:
                subprocess.check_output([timew_binary, "start", interval["start"]]).decode("UTF-8")
        if "end" in interval:
            subprocess.check_output([timew_binary, "stop", interval["end"]]).decode("UTF-8")

    print("\nDone!")
    exit(0)
