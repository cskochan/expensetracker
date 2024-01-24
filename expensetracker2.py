import os, re
from tempfile import NamedTemporaryFile
import shutil, csv
from datetime import datetime

from expenses import Expenses
from balance import Balance

path = ("./monthly_expense_files/")
yearList = sorted([f for f in os.listdir(path) if re.search(r'\d{4}.csv$', f)])

def main():
    balance = Balance()
    entry = Expenses()
    if len(yearList) == 0:
        print("New user.")
        balance.date = dateToDatetime(makeBalanceDate(input("Starting date [MM/DD/YYYY]: ")))
        balance.first, balance.last = float(input("Starting balance: "))
        writeLine(yearFilename(balance.date), makeLine(balance))
    else:
        print("We will add expenses in a minute.")
    
def makeLine(object) -> str:
    if isinstance(object, Balance()):
        return object.date + ", " + object.first + ", " + object.last
    elif isinstance(object, Expenses()):
        return object.date + ", " + object.name + ", " + object.type + ", " + object.amount

def writeLine(file, line) -> None:
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(line)



def readLine2():
    with open('some.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

# If no date provided, reads the last line of the file
def readLine(filename, date = None) -> str:
        with open(filename, mode="r+t", encoding=None) as f:
            for line in f:
                if datetime.strptime(line[:10], "%Y-%m-%d") == date:
                    return line.strip()
                return line.strip()
            
# Send string, and get an appropriate object, whether balance or expenses
def lineToObj(line):
    pass
            
def makeBalanceDate(date) -> str:
    date = date.year, date.month, 1
    temp = date.split("/") # we want balance to start at beginning of month
    date = temp[0] + "/01/" + temp[2]
    return date
            
# Checks that date is valid.
# If so, return Datetime Object. Else return None
def dateToDatetime(date) -> datetime:
    try:
        dt_obj = datetime.strptime(date, "%m/%d/%Y")
        return dt_obj
    except:
        print("This date does not exist. Please try again.")
        return None
    
# File name format: YYYY_MM.csv
def monthFilename(expenseDate) -> str:
    # FIX ME: exp_datetime.month needs to generate two digit numbers below 10
    filename = str(expenseDate.year) + "_" + str(expenseDate.month) + ".csv"
    return filename

# File name format: YYYY.csv
# This file is for acct balance information
def yearFilename(balanceDate) -> str:
    filename = str(balanceDate.year) + ".csv"
    return filename

if __name__== "__main__":
    main()