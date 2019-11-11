# TimeWarrior Database Correction Script

This is the correction script for the interval flattening bug (TI-102).
The script exports all intervals stored, purges the database, and re-enters the intervals.
 
TimeWarrior 1.1.1 or higher correctly enters intervals.

Use this script when you have used
- TimeWarrior earlier than version 1.1.1
- Exclusions

If none of the above applies, you probably do not need to run this script.

## Usage

After making a backup copy of your Timewarrior data by making a copy of all the files in `~/.timewarrior/data`, run this:
```
$ curl -O https://taskwarrior.org/download/timew-dbcorrection.py
$ python timew-dbcorrection.py
...
```
The script may run for a few minutes, depending on your machine and your database complexity.
It shows a progress bar.
Do not kill the script or you will need to restore from your backup. 

If something went wrong during importing your data, try to export your data into a file (e.g. `timew export > data.json`) and check the JSON data.
(The error message from the script might give you a hint on which line to look at.)
When you have fixed your data, rerun the script providing the corrected JSON via the environment variable `TIMEW_EXPORT_DATA`:
```
$ TIMEW_EXPORT_DATA=path/to/data.json python timew-dbcorrection.py
```

## Limitations
This script can only correct for **one** set of exclusions.
If you have changed your exclusions in the past, please contact support@taskwarrior.org.

## Important
!!! YOU ARE STRONGLY ADVISED TO BACKUP YOUR TIMEWARRIOR DATABASE BEFORE RUNNING THIS SCRIPT !!!
