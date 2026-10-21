# Personal Expense Tracker

## 1. Project Overview

The Personal Expense Tracking and Analysis System is a Python-based application that helps users record, manage, and analyze their daily expenses. It provides expense tracking, category-wise organization, data visualization, and financial summaries.

## 2. Objectives

- Record daily expenses with date, category, amount, description, and payment method.
- Allow users to register and log in securely.
- Support adding, viewing, editing, and deleting expenses.
- Store expense data in a MySQL database.
- Analyze spending patterns using Pandas and NumPy.
- Display reports and charts to help users understand their spending.

## 3. Technologies Used

- **Python** — application logic.
- **Streamlit** — user interface.
- **Flask** — expense management API.
- **Node.js and Express** — authentication API.
- **MySQL (Aiven)** — database.
- **Pandas and NumPy** — data analysis.
- **Matplotlib** — charts and visualization.
- **Requests** — communication with the Flask API.

## 4. Main Features

- User registration and login.
- User-specific expense records.
- Add, view, edit, and delete expenses.
- Category-based expense organization.
- Dashboard and reports.
- Expense data visualization.
- Input validation and error handling.
- Authenticated API requests.
- Database-backed storage.
- Expense summaries and category-wise spending analysis.
- Monthly spending trends.
- CSV report download.

## 5. Database Design

The application uses three MySQL tables.

### Users

Stores user account details, password hashes, email verification information, and account creation time.

### Categories

Stores expense category IDs and unique category names.

### Expenses

Stores expense IDs, dates, categories, amounts, descriptions, payment methods, and user IDs.

The `expenses.category_id` column has a verified foreign-key relationship with `categories.category_id`.

The `expenses.user_id` column is nullable. A foreign-key constraint linking it to `users.id` has not been verified.

Database documentation is provided in:

- `schema.sql`
- `ER_Diagram.md`

## 6. Project Structure

```text
PersonalExpenseTracker/
├── main.py
├── app.py
├── database.py
├── schema.sql
├── ER_Diagram.md
├── requirements.txt
├── README.md
├── .gitignore
├── evidence/
└── auth-server/
    ├── server.js
    ├── package.json
    └── package-lock.json
```

**Note:** The `.venv/` directory contains the local Python environment and does not need to be uploaded. The `.env` files contain configuration values and secrets and must not be committed to a public repository. Keep database credentials, authentication secrets, email passwords, and private certificates secure.

## 7. Installation and Setup

### Prerequisites

- Python installed on the system.
- Node.js and npm installed.
- Access to the configured MySQL database.
- Required environment variables configured locally.
- The required database SSL certificate, if applicable.

### Step 1: Open the Project Folder

Open a terminal in the `PersonalExpenseTracker` project directory.

### Step 2: Create and Activate the Python Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Python Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Start the Authentication Server

Open a separate terminal and run:

```powershell
cd auth-server
npm install
node server.js
```

Keep this terminal open.

### Step 5: Start the Flask API

Open another terminal in the main project directory and activate the virtual environment if necessary.

```powershell
cd "$HOME\OneDrive\Documents\PersonalExpenseTracker"
.\.venv\Scripts\Activate.ps1
python app.py
```

The Flask development server should be available at:

`http://127.0.0.1:5000`

Keep this terminal open.

### Step 6: Start the Streamlit Application

Open a third terminal in the main project directory.

```powershell
cd "$HOME\OneDrive\Documents\PersonalExpenseTracker"
.\.venv\Scripts\Activate.ps1
python -m streamlit run main.py
```

Open the local URL displayed in the terminal, usually:

`http://localhost:8501`

Keep the required servers running while using the application.

**Important:** Configure the required environment variables before starting the servers. Never include actual secret values in this README.

## 8. API Endpoints

Base URL for local Flask development: `http://127.0.0.1:5000`

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API and database health |
| GET | `/api/expenses` | Retrieve authenticated user's expenses |
| POST | `/api/expenses` | Add an expense |
| PUT | `/api/expenses/<expense_id>` | Update an expense |
| DELETE | `/api/expenses/<expense_id>` | Delete an expense |

The expense endpoints require a valid Bearer token.

The authentication API is provided separately by the Node.js and Express server.

## 9. Testing

The application has been tested for core expense-management, authentication, and validation functionality.

| Test | Expected Result | Status |
|---|---|---|
| User login | Valid credentials allow access | Passed |
| Add expense | Valid expense is saved | Passed |
| Retrieve expenses | Authenticated request returns HTTP 200 | Passed |
| Negative expense amount | Request returns HTTP 400 | Passed |
| Update nonexistent expense | Request returns HTTP 404 | Passed |
| Delete nonexistent expense | Request returns HTTP 404 | Passed |
| Reports and charts | Expense summaries and visualizations display | Passed |
| CSV export | Report downloads successfully as a CSV file | Verify before submission |

The API also validates expense dates, amounts, and category IDs. Testing evidence should be supported by screenshots where possible.

Update the CSV export status to **Passed** only after confirming that the download works successfully.

## 10. Limitations

- The application requires database connectivity.
- The authentication and Flask services must be available for their respective features.
- The application is intended as an academic project and may require additional security, deployment, and scalability work before production use.
- The application currently relies on a configured MySQL database and local development servers during local execution.

## 11. Future Enhancements

- Monthly budgets and spending limits.
- Recurring expense support.
- Export reports to additional formats, such as PDF.
- Improved financial insights.
- Budget alerts and savings goals.
- More comprehensive automated testing.
- Improved deployment and scalability.

## 12. Conclusion

The Personal Expense Tracker demonstrates the use of Python, Streamlit, Flask, Node.js, Express, and MySQL to build an expense management application. It combines authentication, expense management, validation, database storage, and data analysis in one project. The application helps users organize expenses, understand spending patterns, and review their financial records through summaries, charts, and reports.
