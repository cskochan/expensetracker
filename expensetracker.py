import os
import re
from datetime import datetime

def main():
    # finds most recent expense sheet month for current acct balance info
    path = ("./monthly_expense_files/")
    files = [f for f in os.listdir(path) if re.search(r'\d{4}_\d{2}.csv$', f)]
    try:
        # balance = sorted(files)[-1] along with whatever info we need from
        # the .csv to retrieve the balance
        print(sorted(files)[-1])
    except:
        # no file means we ask for balance and create a new file
        print("Looks like you're new here. Lets get you started.")
        date_input()
        exp_name = "Balance"
        exp_type = "Balance"
        balance = input("How much you currently have: ")
        print("You now have an acct balance of $" + balance + ".")

        

    date_input()
    # option to add either an expense or an income
    picker = False
    while(picker == False):
        print("""1. Expense\n2. Income""")
        is_expense = input("Expense or Income [1 or 2]:")
        if is_expense == "1":
            exp_name = input("What you just bought: ")
            exp_type = input("Which type of expense: ")
            exp_amount = input("Expense amount: ")
            picker = True
            # SUBTRACT EXPENSE TO .CSV HERE
            print("Expense added")
        elif is_expense == "2":
            exp_name = input("Income source: ")
            exp_type = input("One time or regular: ")
            exp_amount = input("Income amount: ")
            picker = True
            # ADD INCOME TO .CSV HERE
            print("Input added")

    print(exp_name + ", " + exp_type + ", " + exp_amount)
    # add this information to the open csv file
    
    # ask if there are any more expenses to add
    # if not, print a summary of expenses breakdown, remaining budget, etc
    # options to include any useful comparisons
        # ex/ last 6 months with the same period last year
        
# Repeats until input is valid.
# Validity is critical because date is used to create and search csv file names
def date_input():
    date_is_valid = False
    while(date_is_valid == False):
        exp_date = input ("Date of Purchase [MM/DD/YYYY]: ")
        exp_datetime = date_check(exp_date)
        if exp_datetime != None:
            date_is_valid = True
    filename = str(exp_datetime.year) + "_" + str(exp_datetime.month) + ".csv"
    open_file(filename)

# Checks that date is valid. If so, return Datetime Object. Else return None
def date_check(date) -> datetime:
    try:
        dt_obj = datetime.strptime(date, "%m/%d/%Y")
        return dt_obj
    except:
        print("This date does not exist. Please try again.")
        return None
        

def open_file(filename) -> None:
    stream = open("./monthly_expense_files/" + filename, mode='w+t', encoding=None)
    print(filename)
    pass

if __name__== "__main__":
    main()