from datetime import datetime
from colorama import Fore, Style
from tabulate import tabulate
import calendar
import os
import csv


MENU = [
    {"text": "Previous month", "value": "prev"},
    {"text": "Next month", "value": "next"},
    {"text": "Add", "value": "add"},
    {"text": "Delete", "value": "delete"},
    {"text": "Exit", "value": "exit"},
]


def main():
    # Get today's date and time
    today = datetime.now()
    month = today.month
    year = today.year

    # Print welcome message
    print(f"{Fore.YELLOW}\n-----------------------------------------")
    print("--------  Welcome to My Budget  ---------")
    print(f"-----------------------------------------{Fore.RESET}")
    print(f"{Style.DIM}{today.strftime('%c')}{Style.RESET_ALL}\n")

    # Main data and menu: loop until exit option is chosen
    while True:

        # print month header
        print(f"\n{year}           {calendar.month_name[month]}\n")

        # get month file path
        directory = get_year_path(year)
        path = get_month_path(directory, month)

        # read and print month data
        headers, table, balance = get_month_data(path)
        print(tabulate(table, headers, tablefmt="rst") + "\n")

        # Print balance => color green for postive and magenta for negative
        if balance >= 0:
            balance_color = Fore.GREEN
        else:
            balance_color = Fore.MAGENTA
        print(f"{balance_color}=> Balance:   $ {balance:,.2f}{Fore.RESET}\n\n")

        # print menu
        for i in range(len(MENU)):
            print(f"{Fore.YELLOW}{i + 1}{Fore.RESET}.{MENU[i]['text']}")

        # get valid user input
        while True:
            choice = input("\nType the option number: ")
            item = validate_menu_input(choice)
            if not item == None:
                break

        # handle menu choice
        match item:
            case "next":
                year, month = next_month(year, month)
            case "prev":
                year, month = prev_month(year, month)
            case "add":
                print(f"Type {Fore.CYAN}cancel{Fore.RESET} to return to main menu.\n")

                color = Fore.WHITE

                while True:
                    # get transaction type
                    trans_type, color = get_transaction_type()
                    if trans_type == "cancel":
                        break

                    # get day
                    day = get_day(year, month, color)
                    if day == "cancel":
                        break

                    # get desc
                    desc = input(f"{color}Description:{Fore.RESET} ").strip()
                    if desc.lower() == "cancel":
                        break

                    # get amount
                    amount = get_amount(trans_type, color)
                    if amount == "cancel":
                        break
                    
                    # get transaction id
                    id = 0
                    with open(path) as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            id = int(row["id"]) + 1

                    # write transaction
                    with open(f"{path}", "a") as file:
                        writer = csv.DictWriter(file, fieldnames=["id", "day", "desc", "amount", "in"])
                        writer.writerow({"id": id, "day": day, "desc": desc, "amount": amount, "in": trans_type})

                    # exit add loop
                    break

            case "delete":
                while True:
                    id_to_delete = input("Type the id of the transaction you want to delete: ").strip().lower()
                    if id_to_delete == "cancel" or delete_transaction(id_to_delete, path):
                        break
            case "exit":
                break


def get_year_path(year):
    # create year directory if it doesn't exists and get path
    path = f"data/{year}"
    exist = os.path.exists(path)

    if not exist:
        os.makedirs(path)

    return path
    

def get_month_path(dir, month):
    # create month file if it doesn't exists and get path
    path = f"{dir}/{month}.csv"
    exist = os.path.exists(path)

    if not exist:
        with open(f"{path}", "a") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "day", "desc", "amount", "in"])
            writer.writeheader()

    return path


def get_month_data(path):
    headers = ["id", "Day", "Description", "Amount"]
    table = []
    balance = 0.0
    
    with open(path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            # sum amounts
            balance = balance + float(row['amount'])
            
            # change colors for in and out
            if row['in'] == 'in':
                row_color = Fore.GREEN
            else:
                row_color = Fore.MAGENTA
            
            # add row to table
            table.append([row['id'], row['day'], row['desc'], f"{row_color}{float(row['amount']):,.2f}{Fore.RESET}"])

    return (headers, table, balance)


def validate_menu_input(choice):
    # get user input and return the chosen option value
    # catch error if input is not an integer from 1 to last item of menu
    try:
        index = int(choice) - 1
        
        if index < 0:
            raise ValueError
        
        print(f"{Fore.YELLOW}=>{MENU[index]['text']}{Fore.RESET}\n")
        
        return MENU[index]["value"]
    except (ValueError, IndexError):
        print(f"{Fore.RED}Input must be a number from 1 to {len(MENU)}{Fore.RESET}")
        return


def next_month(year, month):
    # if month is december, start new year
    if month == 12:
        next_month = 1
        next_year = year + 1
        path = get_year_path(next_year)
    else:
        next_month = month + 1
        next_year = year
        path = get_year_path(year)

    # create month file if it doesn't exist
    get_month_path(path, next_month)

    return (next_year, next_month)


def prev_month(year, month):
    # if january, start previous year on december
    if month == 1:
        prev_month = 12
        prev_year = year - 1
        path = get_year_path(prev_year)
    else:
        prev_month = month - 1
        prev_year = year
        path = get_year_path(year)

    # create month file if it doesn't exist
    get_month_path(path, prev_month)

    return (prev_year, prev_month)


def get_transaction_type(test_input=None):
    while True:
        # test
        if test_input:
            trans = test_input
        else:
            trans = input(f"Type of transaction ({Fore.GREEN}in{Fore.RESET}/{Fore.MAGENTA}out{Fore.RESET}): ").strip().lower()
        
        # validate input
        if trans == "in":
            return (trans, Fore.GREEN)
        elif trans == "out":
            return (trans, Fore.MAGENTA)
        elif trans == "cancel":
            return (trans, Fore.WHITE)
        else:
            print(f"{Fore.RED}Invalid transaction. Type 'in' for 'income' or 'out' for expense.{Fore.RESET}")
            if test_input:
                return


def get_day(year, month, color, test_input=None):
    # print month calendar
    print(f"\n{calendar.month(year, month)}")

    # Loop until day is valid or cancel
    while True:
        # test
        if test_input:
            day = test_input
        else:
            day = input(f"{color}Day:{Fore.RESET} ").strip().lower()
        
        # validate day
        if day == "cancel" or is_day_valid(year, month, day):
            return day

        if test_input:
            return


def is_day_valid(year, month, day):
    # day must be an integer inside the month range
    try:
        d = int(day)
        month_range = calendar.monthrange(year, month)
        if 0 < d <= month_range[1]:
            return True
        else:
            raise ValueError
    except ValueError:
        print(f"{Fore.RED}Invalid day. Check the calendar above.{Fore.RESET}")
        return False


def get_amount(trans_type, color, test_input=None):
    while True:
        # test input
        if test_input:
            amount = test_input
        else:
            amount = input(f"{color}Amount:{Fore.RESET} $").strip().lower()
        
        # validate input
        if amount == "cancel":
            return amount
        else:
            try:
                # format and return a positive or negative float
                if trans_type == "out":
                    amount = f"-{amount}"
                a = float(amount)
                return f"{a:.2f}"
            except ValueError:
                print(f"{Fore.RED}Amount must be numeric.{Fore.RESET}")
        
        if test_input:
            return


def delete_transaction(id, path):

    # validate id
    try:
        id_to_delete = int(id)
    except ValueError:
        print(f"{Fore.RED}Invalid id{Fore.RESET}")
        return False

    # Variables for id existence and to store file data temporarily
    exists = False
    data = []

    # read file, remove row and store updated data on var
    try:
        with open(path) as file:
            reader = csv.DictReader(file)
            for row in reader:
                if id_to_delete == int(row["id"]):
                    exists = True
                else:
                    data.append(row)
    except FileNotFoundError:
        print(f"{Fore.RED}File not found{Fore.RESET}")

    # if id exists, write the file again, with new data
    if exists:
        with open(path, "w") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "day", "desc", "amount", "in"])
            writer.writeheader()
            for row in data:
                writer.writerow({
                    "id": row["id"], 
                    "day": row["day"], 
                    "desc": row["desc"], 
                    "amount": row["amount"], 
                    "in": row["in"]}) 
    else:
        print(f"{Fore.RED}Id not found{Fore.RESET}")

    data.clear()

    return exists


if __name__ == "__main__":
    main()