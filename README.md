# Personal Expense Tracker

A web-based Personal Expense Tracker built using Python, Streamlit, and MySQL to help users manage expenses, organize spending, and understand their financial habits.

## Features

- **Expense Management:** Add, view, update, and delete expenses.
- **Category Management:** Organize expenses by categories.
- **Dashboard:** View expense summaries and spending insights.
- **Data Visualization:** Explore spending patterns using charts.
- **Reports:** Review recorded expenses and expense summaries.
- **Database Integration:** Store and retrieve expense records using MySQL.

## Technologies Used

- Python
- Streamlit
- MySQL
- Pandas
- NumPy
- Matplotlib
- mysql-connector-python

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Vesusree/personal-expense-tracker.git
cd personal-expense-tracker
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

If the repository contains a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Otherwise, install the required packages:

```bash
pip install streamlit pandas numpy matplotlib mysql-connector-python
```

### 4. Configure the database

Configure your MySQL database connection using the required environment variables or Streamlit secrets.

Make sure the database credentials and connection settings match your database configuration.

**Security note:** Never commit database passwords, API keys, or other secrets to GitHub.

### 5. Run the application

If your main application file is `app.py`, run:

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access the application.

## Database

The application uses MySQL to store expense-related information, including expense records and categories.

## Project Purpose

The goal of this project is to make personal expense management easier through organized records, category-wise tracking, visual dashboards, and spending reports.

## Future Improvements

- Monthly budgets and spending limits
- Budget alerts and notifications
- Export reports to CSV or Excel
- Improved financial analytics

## Author

**Vesusree**

GitHub: [Vesusree](https://github.com/Vesusree)

## License

This project is available for educational and personal use. Add a formal license if you intend to distribute it under specific terms.

