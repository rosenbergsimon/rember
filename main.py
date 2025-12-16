import typer
import datetime as dt
import json

CURRENT_DATE = dt.datetime.now()
CURRENT_DATE_STR = CURRENT_DATE.strftime("%Y-%m-%d")
DATA_FILE = "data.json"
app = typer.Typer()

@app.command()
def login(today_date: str = CURRENT_DATE_STR):
    if len(today_date) != 10:
        print("The entered date is not correct format")
        return
    if today_date[4] != "-":
        print("Date is in wrong fomrat")
        return
    with open(f"{DATA_FILE}") as file:
        entries = json.load(file)
    if "dates_login" in entries:
        if today_date in entries["dates_login"]:
            print("You have already logged in for this day.")
            return
        else:
            entries["dates_login"].append(today_date)
            print("Today's date has been entered into the log.")
    else:
        entries["dates_login"] = [today_date]
        print("Today's date has been entered into the log.")
    
    with open(f"{DATA_FILE}", "w") as file:
        json.dump(entries, file, indent=4)

@app.command()
def add(title: str, date: str = CURRENT_DATE_STR):
    if len(date) != 10:
        print("The entered date is not correct format")
        return
    if date[4] != "-":
        print("Date is in wrong fomrat")
        return
    with open(f"{DATA_FILE}") as file:
        data = json.load(file)
    if "entries" not in data:
        data["entries"] = []
    entries = data["entries"]
    prev_length_entries = len(entries)
    new_code = hex(prev_length_entries)[2:]
    new_code = str(new_code)
    entries.append({"code": new_code, "date": date, "title": title})
    data["entries"] = entries
    with open(f"{DATA_FILE}", "w") as file:
        json.dump(data, file, indent=4)
    print(f"The note stored at {title} has been added as note ID {new_code}.")

@app.command()
def view():
    with open(f"{DATA_FILE}") as file:
        data = json.load(file)
    entries = data["entries"]
    notes = [[i["title"].split("."), len(i["title"].split("."))] for i in entries]
    
    while True:
        search = input("Enter a note category to view subclasses of notes, or nothing for the root tree: ")
        length_search = len(search.split("."))
        if search == "":
            length_search = 0
        split_search = search.split(".")
        tree_result = []
        for j in notes:
            if j[1] > length_search:
                if j[0][0:length_search] == split_search:
                    tree_result.append(j[0][length_search])
                if length_search == 0:
                    tree_result.append(j[0][0])
        tree_result_filtered = []

        for l in tree_result:
            if l in tree_result_filtered:
                pass
            else:
                tree_result_filtered.append(l)
        if split_search == [""]:
            print("You entered the root of the note tree. ")
        else:
            print(f"You entered: {search} ")
        if len(tree_result_filtered) == 0:
            print("There are no sub-folders of notes below the above in memory. ")
        for k in tree_result_filtered:
            print(k)

@app.command()
def review():
    with open(f"{DATA_FILE}") as file:
        data = json.load(file)
    string_dates = [i if len(data["dates_login"]) < 35 else i for i in data["dates_login"][-30:]]
    dt_dates = [dt.datetime.strptime(j, "%Y-%m-%d") for j in string_dates]
    dt_dates.sort(reverse=True)
    if dt_dates[0].day != dt.datetime.now().day:
        print("You have not 'logged in' for today yet. ")
        return
    note_entries = [k for k in data["entries"]]
    for l in range(len(note_entries)):
        note_entries[l]["date"] = dt.datetime.strptime(note_entries[l]["date"], "%Y-%m-%d")

    try:
        one_day = dt_dates[1]
    except IndexError:
        one_day = None
    try:
        six_day = dt_dates[6]
    except IndexError:
        six_day = None
    try:
        twenty_one_day = dt_dates[21]
    except IndexError:
        twenty_one_day = None
    review_count = 0
    for i in range(len(note_entries)):
        if one_day and (one_day == note_entries[i]["date"]):
            print(f"Review: {note_entries[i]["title"]}, code {note_entries[i]["code"]}. (One-day old notes)")
            review_count += 1
        if six_day and (six_day == note_entries[i]["date"]):
            print(f"Review: {note_entries[i]["title"]}, code {note_entries[i]["code"]}. (Six-day old notes)")
            review_count += 1              
        if twenty_one_day and (twenty_one_day == note_entries[i]["date"]):
            print(f"Review: {note_entries[i]["title"]}, code {note_entries[i]["code"]}. (Twenty-one day old notes)")
            review_count += 1

    if review_count == 0:
        print("There are no notes to review for today. ")            
        
if __name__ == "__main__":  
    app()
