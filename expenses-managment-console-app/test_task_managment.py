from task_managment import Expense
from task_managment import add_expenses_from_csv, add_new_expense, create_or_save_file, expense_id, load_file, read_ids_from_expenses

def test_persistance(tmpdir):
    with tmpdir.as_cwd():
        filename ='sample.db'
        expenses = [Expense(id=1, description='ziemniak', amount=0.1), Expense(id=2, description='marchew', amount=1.5)]
        create_or_save_file(filename,expenses)
        got = load_file(filename)
    assert got == expenses

def test_overwrite(tmpdir):
    with tmpdir.as_cwd():
        filename ='sample.db'
        expenses = []
        create_or_save_file(filename,expenses)
        new_expenses = [Expense(id=1, description='ziemniak', amount=0.1), Expense(id=2, description='marchew', amount=1.5)]
        create_or_save_file(filename,new_expenses, overwrite=True)
        got = load_file(filename)
    assert got == new_expenses

def test_read_ids():
    expenses = [Expense(id=1, description='ziemniak', amount=0.1), Expense(id=2, description='marchew', amount=1.5)]
    got = read_ids_from_expenses(expenses)
    assert got == {1,2}

def test_first_unused_id():
    ids = {1,3}
    got = expense_id(ids)
    assert got == 2

def test_add_new_id():
    expenses = [Expense(id=1, description='ziemniak', amount=0.1)]
    description='marchew'
    amount=1.5
    got = add_new_expense(description,amount,expenses)
    expected = [Expense(id=1, description='ziemniak', amount=0.1), Expense(id=2, description='marchew', amount=1.5)]
    assert got == expected

def test_load_csv():
    csv_filename = 'test.csv'
    expenses = []
    got = add_expenses_from_csv(csv_filename, expenses)
    expected =[Expense(id=1, description='marchew', amount=1.5)]
    assert got == expected

