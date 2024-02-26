import os, re
from tempfile import NamedTemporaryFile
import shutil, csv
from datetime import date, datetime

path = ("./expense_files/")
if not os.path.isdir(path): os.mkdir(path)
yearList = sorted([f for f in os.listdir(path) if re.search(r'\d{4}.csv$', f)])
def main():
    balance = {}
    balance = welcome(balance)
    dataEntry()
    balance = readLine(-1, needPrev = True)
    print("Your current balance is now: $" + str("{:.02f}".format(balance['last'])))
    dataDisplay()
    print("See you next time!")

def welcome(balance) -> dict:
    today = datetime.now()
    if len(yearList) == 0: # for new users
        print("New user.")
        balance['date'] = dateTest("Starting date [MM/DD/YYYY]: ")
        balance['date'] = dateToFirst(balance['date'])
        balance['first'] = balance['last'] = float(input("Starting balance: "))
        createNewBalSheet(yearFilename(balance), balance)
        writeBalance(0, balance)
    else: # for returning users
        balance = readLine(-1, needPrev = True)
    print("Current balance: $" + str("{:.02f}".format(balance['last'])))
    return balance


def dataEntry():
    entry = {}
    while(True):
        if isYes("New entry? [Y/n]: "):
            print("""1. Expense\n2. Income""")
            choice = isValidChoice("Expense of Income: ", 1, 2)
            if choice == 1:
                entry = newExpense(entry)
            else:
                entry = newIncome(entry)
            writeEntry(monthFilename(entry), entry)
            
            yearFile = yearFilename(entry)
            if yearFile not in yearList:
                balSheetIndex = createNewBalSheet(yearFile)
                oldRow = readLine(balSheetIndex-1, dateToFirst(entry['date']), True)
            else:
                balSheetIndex = yearList.index(yearFile)
                oldRow = readLine(balSheetIndex, dateToFirst(entry['date']), True)
            newRow = updateRow(entry, oldRow)
            writeBalance(balSheetIndex, newRow, entry['amount'])
        else: break

def newExpense(entry) -> dict:
    entry['date'] = dateTest("Entry date [MM/DD/YYYY]: ")
    entry['name'] = input("Entry name: ")
    print("""1. Shelter\n2. Car\n3. Food\n4. Personal\n5. Entertainment\n6. Utilities\n7. Taxes\n8. Misc""")
    entry['type'] = isValidChoice("Entry type: ", 1, 8)
    entry['amount'] = -float(input("Entry amount: "))
    return entry

def newIncome(entry) -> dict:
    entry['date'] = dateTest("Entry date [MM/DD/YYYY]: ")
    entry['name'] = input("Income source: ")
    entry['type'] = "0" 
    entry['amount'] = float(input("Entry amount: "))
    return entry


def dataDisplay():
    while(True):
        if isYes("See data? [Y/n]: "):
            print("""1. Year expenses by type\n2. Year income compared to total expenses""")
            choice = isValidChoice("Selection: ", 1, 2)
            for year in yearList:
                print(" - " + year[slice(0,4)])
            while(True):
                yearSelect = input("Select year: ")
                if yearSelect + ".csv" in yearList: break
                else: print("Choice not available.")
            if choice == "1":
                option1(yearSelect)
            elif choice == "2":
                option2(yearSelect)  
        else: break
                
def option1(year) -> None:
    monthList = sorted([f for f in os.listdir(path) if re.search(year + r'-\d{2}.csv$', f)])
    typeTotal = [0.0]*9
    for filename in monthList:
        with open(path + filename, 'r', newline='') as f:
            reader = csv.DictReader(f, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                typeTotal[int(row['type'])] += -row['amount']
    print("\nExpenses for " + year + ":")
    print("------------------")
    print("Shelter: $" + str("{:.02f}".format(typeTotal[1])))
    print("Car: $" + str("{:.02f}".format(typeTotal[2])))
    print("Food: $" + str("{:.02f}".format(typeTotal[3])))
    print("Personal: $" + str("{:.02f}".format(typeTotal[4])))
    print("Entertainment: $" + str("{:.02f}".format(typeTotal[5])))
    print("Utilities: $" + str("{:.02f}".format(typeTotal[6])))
    print("Taxes: $" + str("{:.02f}".format(typeTotal[7])))
    print("Misc: $" + str("{:.02f}".format(typeTotal[8])))
    print("------------------")

def option2(year) -> None:
    monthList = sorted([f for f in os.listdir(path) if re.search(year + r'-\d{2}.csv$', f)])
    income = 0.0
    expenses = 0.0
    for filename in monthList:
        with open(path + filename, 'r', newline='') as f:
            reader = csv.DictReader(f, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                if row['type'] == "0":
                    income += row['amount']
                else:
                    expenses += -row['amount']
    print("Income: $" + str("{:.02f}".format(income)))
    print("Expenses: $" + str("{:.02f}".format(expenses)))
    if income > expenses:
        print("You saved $" + str("{:.02f}".format(income - expenses)) + " in " + year + ".")
    elif income < expenses:
        print("You spent $" + str("{:.02f}".format(expenses - income)) + " more than you earned in " + year + ".")
    else:
        print("You spent exactly as much as you earned in " + year + ".")
                    
def isYes(prompt) -> bool:
    while(True):
        test = input(prompt)
        if test.lower() == "y" or test == "":
            return True
        elif test.lower() == "n":
            return False
        else:
            print("Invalid entry.")
            
def isValidChoice(prompt, firstOption, lastOption) -> int:
    while(True):
        choice = input(prompt)
        try:
            choice = int(choice)
            if firstOption <= choice <= lastOption:
                return choice
            else:
                raise
        except:
            print("Invalid option.")
        

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
def createNewBalSheet(filename, initBal={'date':'xxxx-01-xx'}) -> int:
    yearList.append(filename)
    yearList.sort()
    year = filename[slice(0,4)]
    month = int(initBal['date'][5:7]) # used for writing very first balance entry
    with open(path + filename, 'a', newline='') as f:
        fieldnames = ['date', 'first', 'last']
        writer = csv.DictWriter(f, fieldnames = fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        blankRow = {'date':'', 'first':'X', 'last':'X'}
        for i in range(month,13):
            if initBal['date']!='xxxx-01-xx' and i == month:
                writer.writerow(initBal)
            else:
                blankRow['date'] = year + '-' + str("{:02d}".format(i)) + '-01'
                writer.writerow(blankRow)
    return yearList.index(filename)

def writeBalance(index, list, amount=0) -> None:
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
                
def dateTest(prompt) -> str:
    while(True):
        date = input(prompt)
        try:
            dtObject = datetime.strptime(date, "%m/%d/%Y")
            strDate = str(dtObject.date())
            if len(yearList) != 0:
                earliestBal = readLine(0, "earliest")
                if strDate < earliestBal['date']:
                    print("Date precedes date of initial balance.")
                    raise
            return strDate
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