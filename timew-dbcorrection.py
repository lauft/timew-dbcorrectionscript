#!/usr/bin/env python

from __future__ import print_function
import subprocess
import os
import json


try:
    input = raw_input
except NameError:
    pass


def get_version():
    return subprocess.check_output(["timew", "--version"]).decode("UTF-8").strip()


if __name__ == "__main__":
    # check version
    version_array = get_version().split(".")
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
- TimeWarrior before version 1.1.1
- exclusions

If none of the above applies, you probably do not need to run this script.

This script will export your stored intervals, purge your database and re-enter
your data such that exclusions will be applied and properly written to the
database. For further information on this see http://timewarrior.net/some/url.

!!! YOU ARE STRONGLY ADVISED TO BACKUP YOUR TIMEWARRIOR DATABASE BEFORE PROCEEDING !!!

""")

    # first chance to bail out
    answer = input("Proceed? [y/N] ")

    if answer != "y" and answer != "Y":
        print("Exiting script")
        exit(0)

    # gather data and print diagnostics
    print("Gathering information...")

    database_path = os.getenv("TIMEWARRIORDB", os.path.expanduser("~/.timewarrior"))
    files = os.listdir(os.path.join(database_path, "data"))

    print("Database path: '%s' (you can change this by setting environment variable TIMEWARRIORDB)" % database_path)
    print("Found files: %s" % ", ".join(files))
    print("")
    print("The script will now extract your data, purge your database, and re-enter your intervals.")

    # last chance to bail out
    answer = input("Proceed? [y/N] ")

    if answer != "y" and answer != "Y":
        print("Exiting script")
        exit(0)

    # export database
    print("Exporting database...")
    intervals = json.loads(subprocess.check_output(["timew", "export"]).decode("UTF-8").strip())

    print("Extracted %d interval(s)" % len(intervals))

    # purge database
    print("Purging database...")

    for file in files:
        print("Deleting " + os.path.join(database_path, "data", file))
        os.remove(os.path.join(database_path, "data", file))

    # import database
    print("Re-importing database...")

    for interval in intervals:
        if "start" in interval:
            print(subprocess.check_output(["timew", "start", interval["start"]]).decode("UTF-8"))
        if "end" in interval:
            print(subprocess.check_output(["timew", "stop", interval["end"]]).decode("UTF-8"))

    print("Done!")
    exit(0)
