"""
Program with a console menu that allows you to save and manage your expenses.


Usage:  Task_managment.py    command subcommand

Commands:
  add           Add a new task. Usage:  add "name" kwota
  clear         Clears the expense base, returns a base containing an empty list...
  exportpython  Prints representation of expenses.
  importcsv     Imports the expense base from a csv file, the file must contain...
                Usage: importcsv filename.csv
  init          Creates an empty expense database file
  show          Prints a list of expenses and their summary. (database preview)

"""


import csv
from dataclasses import dataclass
import pickle
import sys

import click


DB_FILENAME = "expanses_base.db"
EXPENSE_0 = []


@dataclass
class Expense:
    id : int
    description : str
    amount : float
   
    def __post_init__(self):
        if not self.description:
            raise ValueError("Opis wydatku nie może być pusty")
        if type(self.amount) != float:
            raise TypeError("Kwota wydatku musi być liczbą")
        if self.amount <=0:
            raise ValueError("Kwota wydatku musi być dodatnia")
        self.big = True if self.amount >= 1000 else False

    def is_big(self):
        TRESHOLD = 1000
        if self.amount >= TRESHOLD:
            return True
        else:
            return False


def load_file(filename :str) -> list[Expense]:
    try:
        with open(filename,'rb') as stream:
            expenses = pickle.load(stream)
    except FileNotFoundError:
        print_error(13)
        sys.exit(13)
    return expenses


def create_or_save_file(filename :str, expenses :list[Expense], overwrite:bool = False): 
    try:
        if overwrite:
            mode = 'wb'
        else:
            mode = 'xb'
        with open(filename, mode) as stream:
            pickle.dump(expenses,stream)
    except FileExistsError:
        raise FileExistsError


def read_ids_from_expenses(expenses:list[Expense]) -> set[int]:
    ids = {ex.id for ex in expenses}
    return ids


def expense_id(ids:set[int]) -> int:
    """Count first unused id"""
    counter=1
    while counter in ids:
        counter += 1
    return counter


def add_new_expense (description :str, amount :str, expenses :list[Expense]):
    ids = read_ids_from_expenses(expenses)
    id = expense_id(ids)
    try:
        new_expense = Expense(id,description,float(amount))
    except ValueError:
        print_error(21)
        sys.exit(21)
    expenses.append(new_expense)
    return expenses


def add_expenses_from_csv(csv_filename :str,expenses :list[Expense]) -> list[Expense]:
    try:
        with open(csv_filename,'r') as stream:
            new_expenses = csv.DictReader(stream)
            for row in new_expenses:
                add_new_expense(row["description"],row["amount"],expenses)
    except FileNotFoundError:
        print_error(12)
        sys.exit(12)
    return expenses


def print_expense(expense :Expense):
    """Drukuje pojedynczy wydatek z klasy Expense w formie przystępnej dla użytkownika"""
    big = "TAK" if expense.is_big() == True else "-"
    printable_expense = f"{expense.id:<5}{expense.description:40}{expense.amount:<15}{big:10}"
    print(printable_expense)


def print_raport(expenses:list[Expense]):
    """ Drukuje na ekran listę wydatków oraz ich podsumowanie """
    header = f"{'ID:':<5} {'Opis wydatku :':40} {'Kwota :':10} {'Duży wydatek? :':10}"
    sum_ = sum([ex.amount for ex in expenses])
    print("")
    print("--------------------------------------------------------------------------")
    print(header)
    print("--------------------------------------------------------------------------")
    for expense in expenses:
        print_expense(expense)
    print("--------------------------------------------------------------------------")
    print(f"{'SUMA wszystkich wydatków:':^45}{sum_:<10}")


def print_empty_report():
    print()
    print("Nie dodano jeszcze żadnych wydatków.")
    print('Możesz dodać wydatki za pomocą funkcji:   ~add "<wydatek>" <kwota>')


def print_error(err_code :int):
    print("")
    print("BŁĄD:")
    if err_code == 11:
        print("Nie można utworzyć nowej listy wydatków. Lista już istnieje !!!")
        print("(Użyj funkcji 'report' aby ją wyświetlić)")
    elif err_code == 12: 
        print("Nie znaleziono pliku .csv o podanej nazwie")
        print("(Sprawdź czy podałeś właściwą ścieżkę i nazwę pliku.)")
    elif err_code == 13:
        print("Nie znaleziono pliku expenses_base.db")
        print("(Dodaj nowe wydatki za pomocą 'add' lub zainicjuj pustą bazę za pomocą 'init')")
    elif err_code == 21:
        print("Podano niewłaściwą wartość.")
        print("Kwota musi być liczbą, rozdzieloną '.' a wydatek musi zawierać opis.")
    elif err_code == 30:
        print("Wydatek o takim ID nie istnieje.")
        print("Żaden wydatek nie został usunięty.")


@click.group
def cli():
    pass


@cli.command
def exportpython():
    """Wyświetla reprezentację obiektów wydatków"""
    expenses = load_file(DB_FILENAME)
    print("")
    print(f"{expenses!r}")


@cli.command
def init():
    "Tworzy pusty plik z bazą danych wydatków"
    try:
        create_or_save_file(DB_FILENAME, expenses=[])
        print("Pusta baza danych wydatków stworzona!")
    except FileExistsError:
        print_error(11)
        sys.exit(11)


@cli.command
@click.argument("description")
@click.argument("amount")
def add(description :str, amount :float):
    """Dodaj nowe zadanie. Użycie: ~ add 'nazwa wydatku' kwota"""
    expenses = load_file(DB_FILENAME)
    expenses = add_new_expense(description,amount,expenses)
    create_or_save_file(DB_FILENAME,expenses,overwrite=True)
    print("Dodano wydatek!")


@cli.command
def clear():
    """Czyści bazę wydatków, zwraca bazę zawierającą pustą listę wydatków."""
    confirmation = input("""Tej operacji nie można cofnąć.
    Czy potiwerdzasz wyczyszczenie całej bazy wydatków? [Y/N]
    """)
    if confirmation.lower() == 'y' or confirmation.lower() == 'yes': 
        create_or_save_file(DB_FILENAME,expenses=[],overwrite=True)
        print("Operacja zakończona pomyślnie")
        print("Baza wydatków jest pusta")
    else:
        print("Anulowano")
        sys.exit(10)


@cli.command
def show():
    """Drukuje listę wydatków oraz ich podsumowanie."""
    expenses = load_file(DB_FILENAME)
    if expenses:
        print_raport(expenses)
    else:
       print_empty_report()


@cli.command
@click.argument("csv_filename")
def importcsv(csv_filename :str):
    """ Importuje bazę wydatków z pliku csv, plik musi zawierać kolumny: 'nazwa wydatku','kwota'"""
    expenses = load_file(DB_FILENAME)
    new_expenses = add_expenses_from_csv(csv_filename,expenses)
    create_or_save_file(DB_FILENAME, new_expenses, overwrite=True)
    print("Dodano wydatki z pliku .csv")


def main():
    cli()


if __name__ == "__main__":
    main()