#rember

Rember is a CLI tool that keeps track of all the paper/electronic notes you take in school/work/other areas, assigns each a base-16 numerical identifies, and keeps track of the directories, subdirectories, and individual notes. In addition to storing the data for your notes (this could be useful if you have many binders/notebooks/computers containing notes), a feature to review your notes based on the time since initially learning the material is available. This is based on the Ebbinghaus Forgetting Curve's principles that reviewing your learning material approximately one day, a week, and three-to-four weeks assists in information retention. Rember keeps track of the date you learned each note for this.

# Setup

Rember utilizes the Typer CLI library. No other dependencies are required. The program has limited error handling. In the main.py file, change the DATA_FILE global variable to the path of the target JSON file to use for logging all the data, in case you want a different test file or something. 

# Documentation

    python ./main.py login
    python ./main.py login --date <yyyy-mm-dd>

login registers that today is a day you wish to register as a "learning day". Days that aren't logged in to won't count towards the duration since last reviewing a note or material. Optionally you can manually enter in a date, in case you wish to enter a previous date in.

    python ./main.py add <note.path>
    python ./main.py add <note.path> --date <yyyy-mm-dd>
    # example: python ./main.py add math.calculus.limits.introduction --date 2025-12-01

add adds a new note into the JSON file, with a corresponding date. Running add will return the hex number corresponding to that note. Using periods "." should be used as delimeters for "directories".

    python ./main.py view

view allows the viewing of the "directories" of notes logged in the JSON so far. Follow the prompts to enter a directory, and the corresponding subdirectories and files will display. Use periods "." as delimeters. 

    python ./main.py review

review finds out what notes need to be reviewed today. It bases this on by finding what notes are 1, 6, and 21 days old. 