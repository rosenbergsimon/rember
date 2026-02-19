# rember

Rember is a CLI tool that keeps records of all the paper and electronic notes you take for school and work, and assigns each a base-16 numerical identifier. In addition to storing the records for your notes (this could be useful if you have many binders/notebooks/computers containing notes), a feature to review your notes based on the time since initially learning the material is available. This is based on the Ebbinghaus Forgetting Curve's principles that reviewing your learning material approximately one day, a week, and three-to-four weeks assists in information retention. Rember keeps track of the date you learned each note for this.

# Setup

Rember utilizes the Typer CLI library. No other dependencies are required. The program has limited error handling. In the main.py file, change the DATA_FILE global variable to the path of the target JSON file to use for logging all the data, in case you want a different test file or something. To change the days since learning a note to trigger a review advisory instead of the default 1, 6, and 21 days, open the data.json file (the login command needs to have been run at least once before), and change the strings under "review_periods" key. Any length of options is acceptable. 

# Information

Notes are stored in the format of file paths on a computer, so for example you could have a Math directory with a calculus subdirectory, with further subdirectiories for limits, derivativs, chain rule, etc. Each of those could have further individual notes underneath. For example, one note could be stored as math.calculus.limits.introduction. 

# Documentation

    python ./main.py login
    python ./main.py login --date <yyyy-mm-dd>

login registers that today is a day you wish to register as a "learning day". Days that aren't logged in to won't count towards the duration since last reviewing a note or material. Optionally you can manually enter in a date, in case you wish to enter a previous date in.

    python ./main.py add <note.path>
    python ./main.py add <note.path> --date <yyyy-mm-dd>
    # example: python ./main.py add math.calculus.limits.introduction --date 2025-12-01

add adds a new note into the JSON file, with a corresponding date. Running add will return the hex number corresponding to that note. Using periods "." should be used as delimeters for "directories".

    python ./main.py view

view allows the viewing of the "directories" of notes, and their corresponding entries and hex codes which have been logged in the JSON so far. It will display like running the "tree" command on unix. 

    python ./main.py review

review finds out what notes need to be reviewed today.

    python ./main.py delete <note.path>

deletes the note from storage. The id codes for other notes are not changed.