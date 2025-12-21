import typer
import datetime as dt
import json

CURRENT_DATE = dt.datetime.now()
CURRENT_DATE_STR = CURRENT_DATE.strftime("%Y-%m-%d")
DATA_FILE = "data.json"
app = typer.Typer()

@app.command()
def login(date: str = CURRENT_DATE_STR):
    if len(date) != 10:
        print("The entered date is not correct format")
        return
    if date[4] != "-":
        print("Date is in wrong fomrat")
        return
    with open(f"{DATA_FILE}") as file:
        entries = json.load(file)
    if "review_periods" in entries:
        pass
    else:
        entries["review_periods"] = ["1", "6", "21"]
    if "dates_login" in entries:
        if date in entries["dates_login"]:
            print("You have already logged in for this day.")
        else:
            entries["dates_login"].append(date)
            print("Today's date has been entered into the log.")
    else:
        entries["dates_login"] = [date]
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
    highest_id = 0
    for i in entries:
        if int(i["code"], 16) > highest_id:
            highest_id = int(i["code"], 16)
    new_code = hex(highest_id + 1)
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

    dates_list = [int(i) for i in data["review_periods"]]
    dates_to_review = []
    for i in dates_list:
        try:
            dates_to_review.append([i, dt_dates[i]])
        except IndexError:
            pass
    review_count = 0
    for i in range(len(note_entries)):
        for j in dates_to_review:
            if j[1] == note_entries[i]["date"]:
                print(f"Review: {note_entries[i]["title"]}, code {note_entries[i]["code"]}. ({j[0]} day old notes.)")
                review_count += 1

    if review_count == 0:
        print("There are no notes to review for today. ")

@app.command()
def delete(note: str):
    with open(f"{DATA_FILE}") as file:
        data = json.load(file)
    is_present = False
    for i in data["entries"]:
        if i["title"] == note:
            is_present = data["entries"].index(i)
    if not is_present:
        print("This note could not be found. ")
        return
    else:
        print(f"{note} under code {data["entries"][is_present]["code"]} has been deleted.")
        data["entries"].pop(is_present)
    
    with open(f"{DATA_FILE}", "w") as file:
        json.dump(data, file, indent=4)        

if __name__ == "__main__":  
    app()
