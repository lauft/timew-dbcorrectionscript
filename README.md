# TimeWarrior Database Correction Script

Correction script for the interval flattening bug (TI-102).
The script exports all intervals stored, purges the database, and re-enters the intervals.
 
TimeWarrior 1.1.1 or higher should then apply exclusions and write them correctly to the database.

Use this script when you have used
- TimeWarrior before version 1.1.1
- exclusions

If none of the above applies, you probably do not need to run this script.

## Limitations
This script can only correct for **one** set of exclusions.
If you have changed your exclusions in the past, please contact support@taskwarrior.org.

## Important
!!! YOU ARE STRONGLY ADVISED TO BACKUP YOUR TIMEWARRIOR DATABASE BEFORE RUNNING THIS SCRIPT !!!
