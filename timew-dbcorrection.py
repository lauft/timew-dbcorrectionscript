from __future__ import print_function


def get_version():
    return '0.0.0'


if __name__ == "__main__":
    # check version
    version_array = get_version().split(".")
    major_version = int(version_array[0])
    minor_version = int(version_array[1])

    if major_version <= 1 and minor_version == 0:
        print("This script requires TimeWarrior version 1.1.0 or larger!")
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

    # gather data and print diagnostics

    # last chance to bail out

    # export database

    # purge database

    # import database

    exit(0)
