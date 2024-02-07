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
            
            yearFile = yearFilename(entry)
            if yearFile not in yearList:
                balSheetIndex = createNewBalSheet(yearFile)
                newRow = readLine(balSheetIndex-1, dateToFirst(entry['date']), True)
            else:
                balSheetIndex = yearList.index(yearFile)
                newRow = readLine(balSheetIndex, dateToFirst(entry['date']), True)
            newRow = updateRow(entry, newRow)
            writeBalance(balSheetIndex, newRow, entry['amount'])
        else:
            break
    balance = readLine(-1, needPrev = True)
    print("Your current balance is now: $ ", + str("{:.02f}".format(balance['last'])))
    print("See you next time!")

def welcome(balance) -> dict:
    today = datetime.now()
    if len(yearList) == 0: # for new users
        print("New user.")
        while(True):
            balance['date'] = dateTest(input("Starting date [MM/DD/YYYY]: "))
            if balance['date'] != None:
                break
        balance['date'] = dateToFirst(balance['date'])
        balance['first'] = balance['last'] = float(input("Starting balance: "))
        createNewBalSheet(yearFilename(balance), balance)
        print(balance)
        writeBalance(0, balance)
    else: # for returning users
        balance = readLine(-1, needPrev = True)
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
            earliestBal = readLine(0, "earliest")
            if entry['date'] < earliestBal['date']:
                print("Date precedes date of initial balance.")
                raise
            break
        except:
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
            earliestBal = readLine(0, "earliest")
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

# sets values for the newRow entry/adjustment.
def updateRow(entry, oldRow) -> dict:
    newRow = {}
    newRow['date'] = dateToFirst(entry['date'])
    if newRow['date'] == oldRow['date']:
        newRow['first'] = oldRow['first']
    else:
        newRow['first'] = oldRow['last']
    newRow['last'] = oldRow['last'] + entry['amount']
    return newRow
    
# returns index of the newly created, empty file
def createNewBalSheet(filename, initBal={}) -> int:
    yearList.append(filename)
    yearList.sort()
    year = filename[slice(0,4)]
    month = int(date[5:7]) # used for writing very first balance entry
    with open(path + filename, 'a', newline='') as f:
        fieldnames = ['date', 'first', 'last']
        writer = csv.DictWriter(f, fieldnames = fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        blankBal = {'date':'xxxx-01-xx', 'first':'X', 'last':'X'}
        for i in range(month,13):
            if initBal=={}:
                blankBal['date'] = year + '-' + str("{:02d}".format(i)) + '-01'
                writer.writerow(blankBal)
            else:
                writer.writerow(initBal)
    return yearList.index(filename)

def writeBalance(index, list, amount=0):
    fieldnames = ['date', 'first', 'last']
    for i in range(index, len(yearList)): # repeat for all years index and over
        tempfile = NamedTemporaryFile('w+t', newline='', delete=False)
        with open(path + yearList[i], 'r', newline='') as csvFile, tempfile:
            reader = csv.DictReader(csvFile, fieldnames, quoting=csv.QUOTE_NONNUMERIC)
            writer = csv.DictWriter(tempfile, fieldnames, quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            next(reader, None)
            for row in reader:
                if row['date'] < list['date']: # copy existing row
                    writer.writerow(row)
                elif row['date'] == list['date']: # replace old row with new one
                    writer.writerow(list)
                elif row['date'] > list['date']: # update subsequent rows to reflect changes
                    if isinstance(row['first'], float):
                        row['first'] = row['first'] + amount
                        row['last'] = row['last'] + amount
                    writer.writerow(row)
        shutil.move(tempfile.name, path + yearList[i])

def writeEntry(filename, list) -> None:
    new = True if not os.path.exists(path + filename) else False
    fieldnames = ['date', 'name', 'type', 'amount']
    with open(path + filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames = fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        if new == True: writer.writeheader()
        writer.writerow(list)

def readLine(index, date = "XXXX-XX-XX", needPrev = False) -> dict:
    with open(path + yearList[index], 'r', newline='') as f:
        reader = csv.DictReader(f, quoting=csv.QUOTE_NONNUMERIC)
        latestRow = {}
        for row in reader:
            if needPrev and row['date'] <= date: # previous edited row
                if row['first'] != "X":
                    latestRow = row
            elif date == "earliest": # user can't input entries prior to earliest date
                return row
            elif not needPrev and row['date'] == date: # return specific row
                return row
        if latestRow == {}:
            latestRow = readLine(index - 1, date, needPrev)
        return latestRow # for returning last used row of file
                
def dateTest(date = None) -> str:
    try:
        dtObject = datetime.strptime(date, "%m/%d/%Y")
        return str(dtObject.date())
    except:
        print("Please enter valid date.")
        
# Entry dates need to be set to first of month to be compatible with balance sheet
def dateToFirst(date) -> str:
    dateTemp = date
    date = dateTemp[:7] + "-01"
    return date
    
# File name format: YYYY-MM.csv
def monthFilename(expenseDate) -> str:
    date = expenseDate['date']
    filename = date[:7] + ".csv"
    return filename

# File name format: YYYY.csv
def yearFilename(balanceDate) -> str:
    date = balanceDate['date']
    filename = date[:4] + ".csv"
    return filename

if __name__== "__main__":
    main()