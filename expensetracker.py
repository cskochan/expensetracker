from datetime import datetime

def main():
    
    # check for latest csv and read current budget. if no csv, ask for budget
    csv_exists = False
    if csv_exists == False:
        budget = input("How much you currently have: ")
        print("You have $" + budget)
        
    # Date input. Repeats until input is valid.
    # Validity is critical because date is used to create and search csv file names
    date_is_valid = False
    while(date_is_valid == False):
        exp_date = input ("Date of Purchase [MM/DD/YYYY]: ")
        datetime_obj = date_check(exp_date)
        if datetime_obj != None:
            date_is_valid = True
    file_check(exp_date)
    print(datetime_obj.year)
    
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
            print("Expense added")
        elif is_expense == "2":
            exp_name = input("Income source: ")
            exp_type = input("One time or regular: ")
            exp_amount = input("Income amount: ")
            picker = True
            print("Input added")

    print(exp_name + ", " + exp_type + ", " + exp_amount)
    # add this information to the open csv file
    
    # ask if there are any more expenses to add
    # if not, print a summary of expenses breakdown, remaining budget, etc
    # options to include any useful comparisons
        # ex/ last 6 months with the same period last year
        

# Checks that date is valid. If so, return Datetime Object. Else return None
def date_check(date) -> datetime:
    try:
        dt_obj = datetime.strptime(date, "%m/%d/%Y")
        return dt_obj
    except:
        print("This date does not exist. Please try again.")
        return None
        

def file_check(date) -> None:
    # check to make sure file for that month and year exist, if so, open it
    # if not, create it
    print(date)
    pass

if __name__== "__main__":
    main()