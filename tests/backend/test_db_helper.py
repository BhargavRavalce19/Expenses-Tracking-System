from backend import db_helper

def test_fetch_expenses_for_date_aug_15():
    expenses = db_helper.get_expenses_for_date("2024-08-15")

    assert len(expenses) == 1
    assert expenses[0]['amount'] == 10.0
    assert expenses[0]['category'] == "Shopping"
    assert expenses[0]['notes'] == "Bought potatoes"

def test_fetch_expenses_for_date_invalid_date():
    expenses = db_helper.get_expenses_for_date("9999-05-12")

    assert len(expenses) == 0

def test_fetch_expense_summary_invalid_range():
    summary = db_helper.fetch_expense_summary("2009-05-01","2023-01-01")

    assert len(summary) == 0

def test_fetch_expense_raw_date():
    data = db_helper.fetch_expense_raw_date()

    assert len(data) == 3