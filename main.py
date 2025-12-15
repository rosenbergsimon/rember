import typer
import datetime as dt
import json

CURRENT_DATE = dt.datetime.now()
CURRENT_DATE_STR = CURRENT_DATE.strftime("%Y-%m-%d")
DATA_FILE = "test.json"
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
    
    while True:
        print("Enter a note category to view subclasses of notes: \n")


if __name__ == "__main__":  
    app()
