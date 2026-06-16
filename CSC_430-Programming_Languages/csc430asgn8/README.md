## Assignment 8 Details

**GOAL**: Recreate SHEQ4 in COBOL

Note, since COBOL does not have anything like Racket's "Symbols" or "S-expressions", we will simply be parsing strings. Everything else should (hopefully...) be similar in concept?

**REMINDER**: Finishing the project is **not** required for a passing grade. The final grade on this assignment is dependent on the presentation of our learnings of COBOL while working on this assignment!

## Set Up

We're gonna be doing this through bash. So if you're on Mac (Kaitlyn) or Linus (Kenton), idk how to help u tbh but feel free to ask! For my Windows users, we can use Windows Subsystem for Linus (WSL) and Ubuntu + the 'Remote - WLS' extension on VSCode to do our work in VSCode.

I highly recommend doing this on VSCode for now and downloading the following extensions for help:
- *Remote - WLS*
- *COBOL* (by Bitlang)
- *Cobol Language Support* (by Broadcom)

COBOL has very unique syntax and this should hopefully help us get over hurdles more quickly!

Run the followng code in your bash terminal:
```
sudo apt update
sudo apt install gnucobol
```

Next, if you're using VSCode, you can connect your VSCode using Remote - WLS. Open your command palette in VSCode (CTRL + Shift + P) and look for Connect to WSL (or something like that). Then, you can connect to your Ubuntu session!

Then, you can clone this repo set up a new directory! If you're using VSCode, you can clo If you did work in 225 or 357, it's possible you could find directories for those courses here using `ls`.

And voila! Hopefully, everything worked fine. If it didn't msg the discord lol.

## Compiling and Executing basics
Note: COBOL files can end with either `.cbl` or `.cob`. Either should be fine.

To compile a file, type:
```
cobc -x <file_name(.cbl/.cob)>
```
This should create a new file in the directory with just the `<file_name>` without the `(.cob/.cbl)` extension!

To run a compiled file, type:
```
cobcrun <file_name>
```


