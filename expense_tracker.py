import sqlite3
from datetime import date
connection = sqlite3.connect('expenses.db')

cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        description TEXT,
        date TEXT
    )
''')
connection.commit()

while True:
    print()
    print("Welcome to Expense Tracker")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. Edit Expense")
    print("5. Search Expense")
    print("6. Category Summary")
    print("7. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        try:
            amount = float(input("Enter amount: "))
        except ValueError:
            print("Please enter a valid number!")
            continue
        category = input("Enter category: ")
        description = input("Enter description: ")
        expense_date = date.today().strftime('%d-%m-%Y')

        cursor.execute(
            "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
            (amount, category, description, expense_date)
        )

        connection.commit()

        print("Expense added successfully!")

    elif choice == 2:
        cursor.execute("SELECT * FROM expenses")

        rows = cursor.fetchall()

        if len(rows) == 0:
            print("No expenses found!")
        else:
            print("Your Expenses:")

            for row in rows:
                print("ID:", row[0])
                print("Amount:", row[1])
                print("Category:", row[2])
                print("Description:", row[3])
                print("Date:", row[4])
                print("----------------------")

    elif choice == 3:
        cursor.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("No expenses found!")
        else:
            print("Your Expenses:")

            for row in rows:
                print(row[0], "-", row[2], "-", row[1])

            try:
                expense_id = int(input("Enter expense ID to delete: "))
            except ValueError:
                print("Please enter a valid expense ID!")
                continue

            cursor.execute(
                "DELETE FROM expenses WHERE id = ?",
                (expense_id,)
            )

        if cursor.rowcount == 0:
            print("No expense found with this ID!")
        else:
            connection.commit()
            print("Expense deleted successfully!")

    elif choice == 4:
        cursor.execute("SELECT * FROM expenses")
        rows = cursor.fetchall()

        if len(rows) == 0:
            print("No expenses found!")
        else:
            print("Your Expenses:")

            for row in rows:
                print(row[0], "-", row[2], "-", row[1])

            try:
                expense_id = int(input("Enter expense ID to edit: "))
            except ValueError:
                print("Please enter a valid expense ID!")
                continue

            try:
                new_amount = float(input("Enter new amount: "))
            except ValueError:
                print("Please enter a valid number!")
                continue
            new_category = input("Enter new category: ")
            new_description = input("Enter new description: ")

            cursor.execute(
                """UPDATE expenses
                SET amount = ?, category = ?, description = ?
                WHERE id = ?""",
                (new_amount, new_category, new_description, expense_id)
            )

            connection.commit()

            print("Expense edited successfully!")

    elif choice == 5:
        search_category = input("Enter category to search: ")

        cursor.execute(
            "SELECT * FROM expenses WHERE category = ?",
            (search_category,)
        )

        rows = cursor.fetchall()

        if len(rows) == 0:
            print("No expense found for this category!")
        else:
            for row in rows:
                print("ID:", row[0])
                print("Amount:", row[1])
                print("Category:", row[2])
                print("Description:", row[3])
                print("Date:", row[4])
                print("----------------------")

    elif choice == 6:
        cursor.execute("""
            SELECT category, SUM(amount)
            FROM expenses
            GROUP BY category
        """)

        rows = cursor.fetchall()

        if len(rows) == 0:
            print("No expenses found!")
        else:
            print("Category-wise Expense Summary:")

            for row in rows:
                print(row[0], ":", row[1])

    elif choice == 7:
        print("Thank You for using Expense Tracker!")
        break

    else:
        print("Invalid choice!")

connection.close()