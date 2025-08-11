# For CRUD - Create,
#            Retrieve(Use again or call data),
#            Update,
#            Delete

import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logging

logger = setup_logging('db_helper')

@contextmanager
def get_db_cursor(commit = False):
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "expense_manager"
    )

    cursor = connection.cursor(dictionary = True, buffered = True)
    try:
        yield cursor
        if commit:
            connection.commit()
    finally:
        cursor.close()
        connection.close()

def get_all_expenses():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
        for expense in expenses:
            print(expense)

def get_expenses_for_date(expense_date):
    logger.info(f"get_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        expenses = cursor.fetchall()
        return expenses

def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit = True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category:{category}, notes:{notes}")
    with get_db_cursor(commit = True) as cursor:
        cursor.execute("INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
                       (expense_date, amount, category, notes)
                       )

def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start_date :{start_date}, end_date:{end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
                '''SELECT category, SUM(amount) as total
                FROM expenses
                WHERE expense_date
                BETWEEN %s and %s
                GROUP BY category;''',
                (start_date, end_date)
        )
        summary = cursor.fetchall()
    return summary

def fetch_expense_raw_date():
    logger.info(f"fetch_expense_raw_date called")
    with get_db_cursor() as cursor:
        cursor.execute('''SELECT
                YEAR(expense_date) AS year,
                MONTH(expense_date) AS month_num,
                MONTHNAME(expense_date) AS month_name,
                SUM(amount) AS total_amount
            FROM expenses
            GROUP BY year, month_num, month_name
            ORDER BY year, month_num;''')
        data = cursor.fetchall()
    return data

if __name__ == "__main__":

   data = fetch_expense_raw_date()

   for data1 in data:
       print(f"Year:{data1['year']}, Month No:{data1['month_num']}, Month_name:{data1['month_name']}, amount:{data1['total_amount']}")

   print(f"{len(data)}")