import os
import re
from datetime import datetime

path = ("./monthly_expense_files/")
file_list = []
oldest_date = None
newest_record = ""
balance = 0
month_list = sorted([f for f in os.listdir(path) if re.search(r'\d{4}_\d{2}.csv$', f)])
year_list = sorted([f for f in os.listdir(path) if re.search(r'\d{4}.csv$', f)])

def main():
    # finds most recent expense sheet month for current acct balance info
    try:
        # balance = sorted(files)[-1] along with whatever info we need from
        # the .csv to retrieve the balance
        print(year_list)
        # this is to make sure no new file before this is created
        oldest_date = get_date(year_list[0])
        print(oldest_date.date())
        #newest_date = get_date(path + year_list[-1])
        # this is to know which file to pull current budget information from
        balance = get_balance(year_list[-1], new=True)
        print(balance)
    except Exception as e:
        print(e)
        # no file means we ask for balance and create a new file
        print("Looks like you're new here. Lets get you started.")
        change_date = date_input("new")
        yr_filename = create_yr_filename(change_date)
        new_balance = "{:.2f}".format(float(input("How much you currently have: ")))
        write_to_file(yr_filename, str(change_date.date()) + ", " + str(balance) + ", " + str(new_balance))
        balance = new_balance
    print("You have an acct balance of $" + str(balance) + '.')
        
    
    # if date is for a new month, need to write something that collects balance from
    # previous month.
    # Also consider that if then that previous month has a new expense or income
    # added to it, it will change the balance for that month, and the subsequent
    # months will also have to be adjusted accordingly.
    
    # option to add either an expense or an income
    working = True
    while(working == True):
        test = input("New entry? [Y/n]: ")
        if test == "Y" or test == "y":
            print(test)
            new_entry()
        elif test == "N" or test == "n":
            print("Thank you! See you next time.")
            working = False
        else:
            print("Please enter either Y or N.")
    
    
    # ask if there are any more expenses to add
    # if not, print a summary of expenses breakdown, remaining budget, etc
    # options to include any useful comparisons
        # ex/ last 6 months with the same period last year
    
def new_entry() -> None:
    adj_date = date_input()
    mo_filename = create_mo_filename(adj_date)
    yr_filename = create_yr_filename(adj_date)
    # expense or income?
    print("""1. Expense\n2. Income""")
    adjustment_type = input("Expense or Income [1 or 2]:")
    if adjustment_type == "1":
        adjustment_str = append_expense(adj_date)
    elif adjustment_type == "2":
        adjustment_str = append_income(adj_date)
    # need to know if file is new so we can create an entry that includes adjusted balance from previous month
    
    if yr_filename not in year_list:
        print("cant find year. its cool for now. we'll code balance later.")
        
    # if mo_filename not in file_list:
    #     print("searching for future file location")
    #     for i in range(len(file_list)):
    #         # for loop currently not working
    #         print("looking at the moment...")
    #         if mo_filename > file_list[f] and mo_filename < file_list[f+1]:
    #             print("found exactly where the file goes")
    write_to_file(mo_filename, adjustment_str)
    # write_to_file(yr_filename, balance_str)

        # note: we need the amount for math as well as adding a line to the file,
        # so just return the string, and ask for the amount after the function call
def append_expense(adj_date) -> str:
    name = input("What you just bought: ")
    print("""1. Food\n2. Shelter\n3. Fun\n4. Misc""")
    type = input("Which type of expense: ")
    amount = amount_input()
    print("Expense added")
    return str(adj_date.date()) + ", " + name + ", " + type + ", " + str(amount)

def append_income(adj_date) -> str:
    name = input("Income source: ")
    print("""1. One time\n2. Regular""")
    type = input("One time or regular: ")
    amount = amount_input()
    print("Input added")
    return str(adj_date.date()) + ", " + name + ", " + type + ", " + str(amount)

        
# Repeats until input is valid.
# Validity is critical because date is used to create and search csv file names
def date_input(new = "") -> datetime:
    exp_datetime = None
    while(exp_datetime == None):
        if new == "new":
            exp_date = input("Initial date [MM/DD/YYYY]: ")
        else:
            exp_date = input("Date of Purchase [MM/DD/YYYY]: ")
        exp_datetime = date_check(exp_date)
    return exp_datetime

def amount_input() -> float:
    amount = None
    while(amount == None):
        try:   
            amount = float(input("Expense amount: ")) * -1
        except:
            print("Something went wrong. Floats or Ints only please.")
    return amount

# File name format: YYYY_MM.csv
def create_mo_filename(exp_datetime) -> str:
    # FIX ME: exp_datetime.month needs to generate two digit numbers below 10
    mo_filename = str(exp_datetime.year) + "_" + str(exp_datetime.month) + ".csv"
    return mo_filename

# File name format: YYYY.csv
# This file is for acct balance information
def create_yr_filename(exp_datetime) -> str:
    yr_filename = str(exp_datetime.year) + ".csv"
    return yr_filename
    
# Checks that date is valid. If so, return Datetime Object. Else return None
def date_check(date) -> datetime:
    try:
        dt_obj = datetime.strptime(date, "%m/%d/%Y")
        return dt_obj
    except:
        print("This date does not exist. Please try again.")
        return None
        

def write_to_file(filename, content):
    stream = open(path + filename, mode='a', encoding=None)    
    stream.write(content + "\n")
    stream.close()
    print("File updated")
    
def get_date(filename) -> datetime:
    with open(path + filename, mode="r+t", encoding = None) as f:
        date = datetime.strptime(f.readline().split(", ")[0], "%Y-%m-%d")
    return date


def get_balance(filename, date = None, new = False) -> float:
    with open(path + filename, mode="r+t", encoding = None) as f:
        try:
            if new == True:
                for line in f:
                    pass
                acct_balance = "{:.2f}".format(float(line.split(", ")[2]))
            else:
                for line in f:
                    row = f.readline().split(", ")
                    if datetime.strptime(row[0], "%Y-%m-%d") == date:
                        acct_balance = row[2]
            return acct_balance
        except Exception as e:
            print(e)
            print("Code requires either a Datetime or a New parameter.")                    
            
    

if __name__== "__main__":
    main()