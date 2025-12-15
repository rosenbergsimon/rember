import typer
import datetime as dt
import json

CURRENT_DATE = dt.datetime.now()
CURRENT_DATE_STR = CURRENT_DATE.strftime("%Y-%m-%d")
app = typer.Typer()

@app.command()
def login(today_date: str = CURRENT_DATE_STR):
    if len(today_date) != 10:
        print("The entered date is not correct format")
        return
    if today_date[4] != "-":
        print("Date is in wrong fomrat")
        return
    with open("data.json") as file:
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
    
    with open("data.json", "w") as file:
        json.dump(entries, file, indent=4)



@app.command()
def spare():
    pass

if __name__ == "__main__":  
    app()
