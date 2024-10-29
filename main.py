import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)
            
    @classmethod
    def add_entry(cls, date, amount, category, description):
        formatted_date = datetime.strptime(date, cls.FORMAT).strftime(cls.FORMAT)
    
        new_entry = {
            "date": formatted_date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(
                f"Transactions from {start_date.strftime(CSV.FORMAT)} to {
                    end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"][
                "amount"
            ].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"][
                "amount"
            ].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df

    @classmethod
    def update_entry(cls, date, amount, new_amount=None, new_category=None, new_description=None):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)

        amount = float(amount)

        mask = (df["date"].dt.strftime(cls.FORMAT)
            == date) & (df["amount"] == amount)

        print(f"Searching for date: {date} and amount: {amount}")
        print(f"Entries in DataFrame:\n{df}")

        if df[mask].empty:
            print("No matching entry found to update.")
            return

        if new_amount is not None:
            df.loc[mask, "amount"] = new_amount
        if new_category is not None:
            df.loc[mask, "category"] = new_category
        if new_description is not None:
            df.loc[mask, "description"] = new_description

        df["date"] = df["date"].dt.strftime(cls.FORMAT)
        df.to_csv(cls.CSV_FILE, index=False)
        print("Entry updated successfully.")
        
    @classmethod
    def delete_entry(cls, date, amount):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        mask = (df["date"].dt.strftime(cls.FORMAT) == date) & (df["amount"] == amount)
    
        if df[mask].empty:
            print("No matching entry found to delete.")
            return

        df = df[~mask]
    
        # Преобразуем даты обратно в нужный формат перед сохранением
        df["date"] = df["date"].dt.strftime(cls.FORMAT)
        df.to_csv(cls.CSV_FILE, index=False)
        print("Entry deleted successfully.")
    
def add():
    CSV.initialize_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ",
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)


def plot_transactions(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index,
             expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    """Main function to run the finance tracker."""
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Delete a transaction")
        print("4. Update a transaction")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            date = get_date(
                "Enter the date of the transaction to delete (dd-mm-yyyy): ")
            amount = get_amount()  # Get the amount directly
            CSV.delete_entry(date, amount)
        elif choice == "4":
            date = get_date(
                "Enter the date of the transaction to update (dd-mm-yyyy): ")
            amount = get_amount()  # Get the amount directly
            new_amount = input(
                "Enter the new amount (leave blank to keep current): ")
            new_category = input(
                "Enter the new category (leave blank to keep current): ")
            new_description = input(
                "Enter the new description (leave blank to keep current): ")

            # Convert new_amount to float if provided
            new_amount = float(new_amount) if new_amount else None
            # Convert new_category using the get_category function if provided
            new_category = get_category() if new_category in [
                "I", "E"] else None
            # Use the existing description if new_description is not provided
            new_description = new_description if new_description else None

            CSV.update_entry(date, amount, new_amount,
                             new_category, new_description)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main()
