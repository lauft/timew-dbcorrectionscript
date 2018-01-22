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
    # export database

    # purge database

    # import database

    exit(0)
