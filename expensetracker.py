import os
import re
from datetime import datetime

def main():
    # finds most recent expense sheet month for current acct balance info
    balance = 0
    oldest_record = ""
    newest_record = ""
    path = ("./monthly_expense_files/")
    files = [f for f in os.listdir(path) if re.search(r'\d{4}_\d{2}.csv$', f)]
    
    try:
        # balance = sorted(files)[-1] along with whatever info we need from
        # the .csv to retrieve the balance
        file_list = sorted(files)
        print(file_list)
        oldest_record = file_list[0]
        print(oldest_record)
        newest_record = file_list[-1]
        print(newest_record)
        for line in open(path + newest_record, mode = "r+t", encoding = None):
            line_list = line.split(", ")
            if line_list[2] == "Balance":
                balance = line_list[3]
    except Exception as e:
        # no file means we ask for balance and create a new file
        print(e)
        print("Looks like you're new here. Lets get you started.")
        change_date = date_input("new")
        filename = create_filename(change_date)
        name = "Starting"
        type = "Balance"
        balance = input("How much you currently have: ")
        exp_or_in = "Balance" #expense or income, uniquely named balance as this is initial balance for month
        write_to_file(filename, str(change_date.date()) + ", " + name + ", " + type + ", " + str(balance) + ", " + exp_or_in)
    print("You have an acct balance of $ " + str(balance) + ".")
        
    
    # if date is for a new month, need to write something that collects balance from
    # previous month.
    # Also consider that if then that previous month has a new expense or income
    # added to it, it will change the balance for that month, and the subsequent
    # months will also have to be adjusted accordingly.
    
    # option to add either an expense or an income
    picker = True
    while(picker == True):
        picker = new_entry()
    
    # add this information to the open csv file
    
    # ask if there are any more expenses to add
    # if not, print a summary of expenses breakdown, remaining budget, etc
    # options to include any useful comparisons
        # ex/ last 6 months with the same period last year
    
def new_entry() -> bool:
    adj_date = date_input()
    filename = create_filename(adj_date)
    print("""1. Expense\n2. Income""")
    adjustment_type = input("Expense or Income [1 or 2]:")
    if adjustment_type == "1":
        adjustment_str = append_expense(adj_date)
    elif adjustment_type == "2":
        adjustment_str = append_income(adj_date)
    write_to_file(filename, adjustment_str)
    if input("New entry? [Y/n]: ") != "Y" or "y":
        print("Thank you! See you next time.")
        return False
    else:
        return True
        
def append_expense(adj_date) -> str:
    name = input("What you just bought: ")
    print("""1. Food\n2. Shelter\n3. Fun\n4. Misc""")
    type = input("Which type of expense: ")
    amount = input("Expense amount: ")
    exp_or_in = "Expense"
    adjust_balance(amount * -1)
    print("Expense added")
    return str(adj_date.date()) + ", " + name + ", " + type + ", " + str(amount) + ", " + exp_or_in

def append_income(adj_date) -> str:
    name = input("Income source: ")
    print("""1. One time\n2. Regular""")
    type = input("One time or regular: ")
    amount = input("Income amount: ") 
    exp_or_in = "Income"
    adjust_balance(amount)
    print("Input added")
    return str(adj_date.date()) + ", " + name + ", " + type + ", " + str(amount) + ", " + exp_or_in

def adjust_balance(amount):
    
    pass

    

        
# Repeats until input is valid.
# Validity is critical because date is used to create and search csv file names
def date_input(new = "") -> datetime:
    date_is_valid = False
    while(date_is_valid == False):
        if new == "new":
            exp_date = input("Today's date [MM/DD/YYYY]: ")
        else:
            exp_date = input("Date of Purchase [MM/DD/YYYY]: ")
        exp_datetime = date_check(exp_date)
        if exp_datetime != None:
            date_is_valid = True
    return exp_datetime

# File name format: YYYY_MM.csv
def create_filename(exp_datetime) -> str:
    filename = str(exp_datetime.year) + "_" + str(exp_datetime.month) + ".csv"
    return filename

# Checks that date is valid. If so, return Datetime Object. Else return None
def date_check(date) -> datetime:
    try:
        dt_obj = datetime.strptime(date, "%m/%d/%Y")
        return dt_obj
    except:
        print("This date does not exist. Please try again.")
        return None
        

def write_to_file(filename, content):
    stream = open("./monthly_expense_files/" + filename, mode='a', encoding=None)
    stream.write(content + "\n")
    stream.close()
    print("File updated")

if __name__== "__main__":
    main()