# TimeWarrior Database Correction Script

Correction script for the interval flattening bug (TI-102).
The script exports all intervals stored, purges the database, and re-enters the intervals.
 
TimeWarrior 1.1.1 or higher should then apply exclusions and write them correctly to the database.

Use this script when you have used
- TimeWarrior before version 1.1.1
- exclusions

If none of the above applies, you probably do not need to run this script.

## Important
!!! YOU ARE STRONGLY ADVISED TO BACKUP YOUR TIMEWARRIOR DATABASE BEFORE RUNNING THIS SCRIPT !!!
