def main():
    
    # check for latest csv and read current budget. if no csv, ask for budget
    csv_exists = False
    if csv_exists == False:
        budget = input("How much you currently have: ")
        print("You have $" + budget)
        
    date_is_valid = False
    while(date_is_valid == False):
        exp_date = input ("Date of Purchase [MM/DD/YYYY]: ")
        date_is_valid = date_check(exp_date)
    file_check(exp_date)
    
    # option to add either an expense or an income?
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

def date_check(date) -> bool:
    # check to make sure that date is valid, and if so, return True
    return True

def file_check(date):
    # check to make sure file for that month and year exist, if so, open it
    # if not, create it
    print(date)
    pass

if __name__== "__main__":
    main()