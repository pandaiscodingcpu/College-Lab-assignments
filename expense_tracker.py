import json
import os
from functools import reduce
import matplotlib.pyplot as plt
# custom exception to check the valid date
class DataNotFound(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code
        super().__init__(message)

    def __str__(self):
        return f"{self.message} (Error Code: {self.code})"

class ExpenseBook:
    def __init__(self, date, description, category, price, paidBy):
        self.date = date
        self.description = description
        self.category = category
        self.price = price
        self.paidBy = paidBy

    def readJson(self):
        if not os.path.exists("expenses.json"):
            raise DataNotFound("No expenses.json file found", 404)
        with open("expenses.json", "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    data = [data]
            except json.JSONDecodeError:
                raise DataNotFound("File is empty or corrupted", 400)
        return data
    def toDict(self):
        return {
            "date": self.date,
            "description": self.description,
            "category": self.category,
            "amount": self.price,
            "who_paid": self.paidBy
        }
    def storeToJson(self):
        expenses = []
        if os.path.exists("expenses.json"):
            with open("expenses.json", "r") as f:
                try:
                    expenses = json.load(f)
                    if isinstance(expenses, dict):
                        expenses = [expenses]
                except json.JSONDecodeError:
                    expenses = []
        expenses.append(self.toDict())
        with open("expenses.json", "w") as f:
            json.dump(expenses, f, indent=4)
    @staticmethod
    def displayFormattedSheet():
        try:
            with open("expenses.json", "r") as f:
                data = json.load(f)
            if isinstance(data, dict):
                data = [data]
            print("\n====== Expense Records ======\n")
            for i, expense in enumerate(data, start=1):
                print(f"Expense #{i}")
                print(f" Date        : {expense.get('date', '-')}")
                print(f" Description : {expense.get('description', '-')}")
                print(f" Category    : {expense.get('category', '-')}")
                print(f" Amount      : Rs.{expense.get('amount', 0)}")
                print(f" Who Paid    : {expense.get('who_paid', '-')}")
                print("-" * 35)
        except FileNotFoundError:
            print("No expenses.json file found.")
        except json.JSONDecodeError:
            print("File is empty or not valid JSON.")

    def addExpense(self):
        pass # we can use directly the storeToJson() function.
    def removeExpense(self, date_str):
        """
        Remove all expenses with matching date from JSON file.
        Returns number of removed expenses.
        """
        if not os.path.exists("expenses.json"):
            raise DataNotFound("No expenses.json file found", 404)

        with open("expenses.json", "r") as f:
            try:
                data = json.load(f)
                if isinstance(data, dict):
                    data = [data]
            except json.JSONDecodeError:
                raise DataNotFound("File is empty or corrupted", 400)

        original_count = len(data)

        # Filter out expenses with the given date
        data = list(filter(lambda e: e.get("date") != date_str, data))

        removed_count = original_count - len(data)

        # Save back updated data
        with open("expenses.json", "w") as f:
            json.dump(data, f, indent=4)
        return removed_count

    def calculateAvg(self):
        data = self.readJson()
        if not data:
            return 0
        avg_expense = 0.0
        total_amount = reduce(lambda acc, e: acc + e.get("price", 0), data, 0)
        avg_expense = total_amount / len(data)
        return f"Rs. {avg_expense}"

    def visualize(self):
        data = self.readJson()  # should return list of dicts
        if not data:
            return "No data in JSON"

        # Extract x and y
        x = [e.get("date", "") for e in data]  # dates on x-axis
        y = [e.get("amount", 0) for e in data]  # amounts on y-axis
        plt.figure(figsize=(10, 5))
        plt.plot(x, y, marker='o', linestyle='-', color='blue')
        plt.xlabel("Date")
        plt.ylabel("Amount (in Rs.)")
        plt.title("Expenses Over Time")
        plt.xticks(rotation=45)  # rotate x labels for better readability
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    print("WELCOME TO EXPENSE TRACKER.....")
    while True:
        print("Choose your option:\n1. Add Expense\n2. Remove Expense\n3. Show Expense\n4. Visualize\n5. Average the expense\n6. Exit")
        try:
            choice = int(input())
            if choice == 1:
                date = str(input("Enter date(DD-MM-YYYY): "))
                description = str(input("Enter description: "))
                category = str(input("Enter the category of the item: "))
                price = int(input("Enter the amount in Rs.: "))
                paidBy = str(input("Amount paid by: "))
                e = ExpenseBook(date, description, category, price, paidBy)
                e.storeToJson()
                continue
            elif choice == 2:
                date = str(input("Enter date(DD-MM-YYYY) to be removed: "))
                e = ExpenseBook("", "", "", 0, "")  # dummy instance to call removeExpense
                removed = e.removeExpense(date)
                print(f"{removed} expense(s) removed.")
                continue
            elif choice == 3:
                ExpenseBook.displayFormattedSheet()
                continue
            elif choice == 4:
                e = ExpenseBook("", "", "", 0, "")  # dummy instance to call visualize
                e.visualize()
                continue
            elif choice == 5:
                e = ExpenseBook("", "", "", 0, "")  # dummy instance to call calculateAvg
                avg = e.calculateAvg()
                print("Average:", avg)
                continue
            elif choice == 6:
                print("Exiting.....")
                break
            else:
                print("Invalid choice. Please select a valid option.")
        except TypeError as e:
            print(e)