import os, re
from tempfile import NamedTemporaryFile
import shutil, csv
from datetime import date, datetime

path = ("./monthly_expense_files/")
yearList = sorted([f for f in os.listdir(path) if re.search(r'\d{4}.csv$', f)])
def main():
    
    balance = {}
    entry = {}
    
    balance = welcome(balance)
    while(True):
        if entryTest() == True:
            if isExpense() == True:
                entry = newExpense(entry)
            else:
                entry = newIncome(entry)
            writeEntry(monthFilename(entry), entry)
            prevBalance = readLine(getPrevBalSheet(yearFilename(entry)), dateToFirst(entry['date']))
            print(prevBalance)
            newBalance = makeNewBalDict(entry, prevBalance)
            
            # the below writeLine() call only appends the file, doesn't replace.
            # i'll write the adjustBalances() function, and have it do
            # this part at the same time.
            #writeLine(path + yearFilename(newBalance['date']), newBalance, entry['amount'])
            # have to find subsequent entries and adjust them with new information
            
            writeBalance(yearFilename(newBalance), newBalance, entry['amount'])
        else:
            break

        # get current balance
        # get user input for next entry
        # calculate new balance
        # add entry
            # 1. (current month)
                # add to existing file
            # 2. (new month)
                # create new file and add to that
                # entry to yearly file
                    # 1. (current year)
                        # add to existing file
                    # 2. (new year)
                        # create new file and add to that
            # 3. (old month)
                # add to existing month file
                # adjust balance for that month and all subsequent months
                    # check for subsequent year files and adjust those too
        # if no more entrys ask about ways to display existing data
            # expenses for month by type, monthly comparisons, etc
    print("Goodbye.")

def welcome(balance) -> dict:
    if len(yearList) == 0: # for new users
        print("New user.")
        while(True):
            balance['date'] = dateTest(input("Starting date [MM/DD/YYYY]: "))
            if balance['date'] != None:
                break
        balance['date'] = dateToFirst(balance['date'])
        balance['first'] = balance['last'] = float(input("Starting balance: "))
        writeBalance(yearFilename(balance), balance)
    else: # for returning users
        balance = readLine(yearList[-1])
        #balance.date, balance.first, balance.last = readLine(path + yearList[-1])
        print(balance['last'])
        balance['date'] = balance['date']
    print("Current balance: $" + str("{:.02f}".format(balance['last'])))
    return balance

def entryTest() -> bool:
    while(True):
        test = input("New entry? [Y/n]: ")
        if test == "Y" or test == "y" or test == "":
            return True
        elif test == "N" or test == "n":
            return False
        else:
            print("Invalid entry.")

def isExpense():
    while(True):
        print("""1. Expense\n2. Income""")
        entry_type = input("Expense or Income [1 or 2]:")
        if entry_type == "1":
            return True
        elif entry_type == "2":
            return False
        else:
            print("Invalid entry.")

def newExpense(entry) -> dict:
    while(True):
        try:
            entry['date'] = dateTest(input("Entry date [MM/DD/YYYY]: "))
            earliestBal = readLine(yearList[0], "earliest")
            if entry['date'] < earliestBal['date']:
                print("Date precedes date of initial balance.")
                raise
            break
        except Exception as e:
            print(e)
            print("Please enter valid date.")
    entry['name'] = input("Entry name: ")
    print("""1. Food\n2. Shelter\n3. Fun\n4. Misc""")
    entry['type'] = input("Entry type: ")
    entry['amount'] = -float(input("Entry amount: "))
    return entry

def newIncome(entry) -> dict:
    while(True):
        try:
            entry['date'] = dateTest(input("Entry date [MM/DD/YYY]: "))
            earliestBal = readLine(yearList[0], "earliest")
            if entry['date'] < earliestBal['date']:
                print("Date precedes date of initial balance.")
                raise
            break
        except:
            print("Please enter valid date.")
    entry['name'] = input("Income source: ")
    entry['type'] = "0"
    entry['amount'] = -float(input("Entry amount: "))
    return entry

# the below code sets values for the newBalance entry/adjustment.
def makeNewBalDict(entry, prevBalance) -> dict:
    newBalance = prevBalance
    newBalance['date'] = dateToFirst(entry['date'])
    if newBalance['date'] == prevBalance['date']:
        newBalance['first'] = prevBalance['first']
    else:
        newBalance['first'] = prevBalance['last']
    newBalance['last'] = newBalance['last'] + entry['amount']
    return newBalance

    
def getPrevBalSheet(filename):
    if filename not in yearList:
        print("getPrevBalSheet yearList: ")
        print(yearList)
        yearList.append(filename)
        sorted(yearList)
        return yearList[yearList.index(filename)-1]
    else:
        return filename
    
"""     for i in range(len(yearList)):
        print(yearList[i])
        if filename < yearList[i]:
            print(yearList[i-1])
            return yearList[i-1]
        return yearList[i] """
            
# This is for finding an entry in the middle of a ####.csv file, inserting it,
# and replacing all subsequent balance entries with entries mathed up to
# reflect the changes.
def writeBalance(filename, list, amount=0):
    tempfile = NamedTemporaryFile('w+t', newline='', delete=False)
    fieldnames = ['date', 'first', 'last']
    if filename not in yearList:
        yearList.append(filename)
        sorted(yearList)
        with open(path + filename, 'a'): os.utime(path + filename, None)
        print("this is where the file is created")
        print("also here is the yearList: ")
        print(yearList)
    for i in range(len(yearList)):
        if yearList[i] >= filename:
            with open(path + yearList[i], 'r', newline='') as csvFile, tempfile:
                reader = csv.DictReader(csvFile, fieldnames, quoting=csv.QUOTE_NONNUMERIC)
                writer = csv.DictWriter(tempfile, fieldnames, quoting=csv.QUOTE_NONNUMERIC)
                writer.writeheader()
                next(reader, None)
                for row in reader:
                    if row['date'] > list['date']:
                        writer.writerow(list)
                        list['date'] = row['date']
                        list['first'] = list['last']
                        print(row['first'])
                        list['last'] = row['first'] + amount
                writer.writerow(list)
            shutil.move(tempfile.name, path + filename)
        else: print("if statement does not run")

def writeEntry(filename, list) -> None:
    new = True if not os.path.exists(path + filename) else False
    with open(path + filename, 'a', newline='') as f:
        fieldnames = ['date', 'name', 'type', 'amount']
        writer = csv.DictWriter(f, fieldnames = fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        if new == True: writer.writeheader()
        writer.writerow(list)


# If no date provided, reads last line of file
def readLine(filename, date = '3000-01-01') -> dict:
    with open(path + filename, 'r', newline='') as f:
        reader = csv.DictReader(f, quoting=csv.QUOTE_NONNUMERIC)
        prevRow = {}
        for row in reader:
            if date == "earliest":
                return row
            elif row['date'] > date:
                if prevRow == {}:
                    print("PrevRow equaled nothing.")
                    #return readLine(yearList[yearList.index(filename)-1], date)
                return prevRow
            prevRow = row
        return prevRow
            
            
# Checks that date is valid.
def dateTest(date = None) -> str:
    try:
        dtObject = datetime.strptime(date, "%m/%d/%Y")
        print("Test dateTest function: " + str(dtObject.date()))
        return str(dtObject.date())
    except:
        print("Please enter valid date.")

def dateToFirst(date) -> str:
    dateTemp = date
    date = dateTemp[:7] + "-01"
    print("Adjusted date: " + date)
    return date
    
    
# File name format: YYYY-MM.csv
def monthFilename(expenseDate) -> str:
    date = expenseDate['date']
    filename = date[:7] + ".csv"
    return filename

# File name format: YYYY.csv
# This file is for acct balance information
def yearFilename(balanceDate) -> str:
    date = balanceDate['date']
    filename = date[:4] + ".csv"
    return filename

if __name__== "__main__":
    main()