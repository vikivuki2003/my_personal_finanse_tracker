# My Personal Finance Tracker

My Personal Finance Tracker is a Python-based application designed to help users manage their personal finances effectively. 
This application allows users to track their income and expenses, generate reports, and visualize financial data over time.

## **Features**

- **Add Transactions**: Easily log income and expenses with detailed descriptions.
- **View Transactions**: Filter and view transactions within a specified date range.
- **Update Transactions**: Modify existing transaction details.
- **Delete Transactions**: Remove unwanted transactions from your records.
- **Visualizations**: Plot income and expenses over time for better insights.
- **CSV Storage**: All data is stored in a CSV file for easy access and management.

## **Technologies Used**

- **Programming Language**: Python
- **Libraries**:
  - `pandas` for data manipulation and analysis
  - `matplotlib` for data visualization
  - `csv` for handling CSV file operations
- **Data Storage**: CSV files

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   git clone https://github.com/vikivuki2003/my_personal_finanse_tracker.git
   cd my_personal_finanse_tracker
   
2. Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3.Install the required packages:
pip install -r requirements.txt


## Usage

Run the application:
python main.py

Follow the prompts to add, view, update, or delete transactions.
You can visualize your income and expenses by selecting the appropriate options in the menu.
Functions Overview
- add(): Prompts the user to enter transaction details and adds them to the CSV file.
- get_transactions(start_date, end_date): Retrieves transactions within a specified date range and provides a summary of total income, expenses, and net savings.
- update_entry(date, amount): Updates an existing transaction based on date and amount.
- delete_entry(date, amount): Deletes a transaction based on date and amount.
- plot_transactions(df): Visualizes income and expenses over time using Matplotlib.
