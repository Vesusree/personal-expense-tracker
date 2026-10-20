
# Personal Expense Tracker

A Python-based Personal Expense Tracking and Analysis System built using Streamlit, Flask, Node.js, and MySQL. It helps users record, manage, and analyze their daily expenses.

## 1. Project Overview

The application provides expense tracking, category-wise organization, data visualization, and financial summaries. It includes user authentication and stores expense records in a MySQL database.

## 2. Objectives

- Record daily expenses with dates, categories, amounts, descriptions, and payment methods.
- Allow users to register and log in securely.
- Support adding, viewing, editing, and deleting expenses.
- Store expense data in a MySQL database.
- Analyze spending patterns using Pandas and NumPy.
- Display reports and charts to help users understand their spending.

## 3. Technologies Used

- **Python** — application logic
- **Streamlit** — user interface
- **Flask** — expense management API
- **Node.js and Express** — authentication server
- **MySQL (Aiven)** — database
- **Pandas and NumPy** — data analysis
- **Matplotlib** — charts and visualization
- **Requests** — communication with the Flask API
- **PyJWT** — JWT authentication

## 4. Main Features

- User registration and login
- Email verification
- Secure password hashing
- User-specific expense records
- Add, view, edit, and delete expenses
- Category-based expense organization
- Dashboard, reports, and visualizations
- Input validation and error handling
- Authenticated API requests
- Database-backed storage

## 5. Database Design

The application uses three MySQL tables.

### Users

Stores user account details, password hashes, email verification information, and account creation time.

### Categories

Stores category IDs and unique category names.

### Expenses

Stores expense IDs, dates, categories, amounts, descriptions, payment methods, and user IDs.

The `expenses.category_id` column has a verified foreign-key relationship with `categories.category_id`.

The `expenses.user_id` column is nullable. A foreign-key constraint linking it to `users.id` has not been verified.

Database documentation:

- `schema.sql`
- `ER_Diagram.md`

An ER diagram image can also be included if available.

## 6. Project Structure

```text
personal-expense-tracker/
├── auth-server/
│   ├── server.js
│   ├── package.json
│   ├── package-lock.json
│   └── ca.pem
├── main.py
├── app.py
├── database.py
├── requirements.txt
├── schema.sql
├── ER_Diagram.md
├── README.md
└── .gitignore
```

Local environment files, virtual environments, and generated files may also exist but should not be committed to the repository.

**Security:** Never upload `.env` files, passwords, JWT secrets, email credentials, or other private credentials to GitHub.

## 7. Installation and Setup

### Prerequisites

- Python 3
- Node.js and npm
- Access to the configured MySQL database
- Required environment variables
- The database SSL certificate, if required by the database configuration

### Step 1: Open the project folder

Open a terminal in the project root.

### Step 2: Create and activate a Python virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Python dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Configure the environment variables expected by `database.py`, `app.py`, and `auth-server/server.js`.

The Python application and authentication server may use separate `.env` files. Use your local configuration and do not commit these files.

### Step 5: Start the authentication server

Open a terminal in the project root and run:

```powershell
cd auth-server
npm install
node server.js
```

Keep this terminal running.

### Step 6: Start the Flask API

Open another terminal in the project root:

```powershell
.\.venv\Scripts\Activate.ps1
python -m flask --app app run --port 5000
```

Keep this terminal running.

### Step 7: Start the Streamlit application

Open a third terminal in the project root:

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run main.py
```

Open the local URL displayed in the terminal.

The authentication server, Flask API, and Streamlit application must be running for the corresponding features to work.

## 8. API Endpoints

Local Flask API base URL:

`http://127.0.0.1:5000`

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API and database health |
| GET | `/api/expenses` | Retrieve the authenticated user's expenses |
| POST | `/api/expenses` | Add an expense |
| PUT | `/api/expenses/<expense_id>` | Update an expense |
| DELETE | `/api/expenses/<expense_id>` | Delete an expense |

Expense endpoints require a valid Bearer token.

## 9. Testing

The following API tests were performed.

| Test | Expected result | Observed result |
|---|---|---|
| Authenticated expense retrieval | HTTP 200 | Passed |
| Negative expense amount | HTTP 400 | Passed |
| Invalid expense date | HTTP 400 | Passed |
| Unknown category ID | HTTP 400 | Passed |
| Update nonexistent expense | HTTP 404 | Passed |
| Delete nonexistent expense | HTTP 404 | Passed |

The API also validates expense amounts, dates, category IDs, and other expense fields.

## 10. Security Notes

- Passwords are stored as hashes.
- Email verification is implemented in the authentication flow.
- Expense API queries are scoped to the authenticated user.
- API requests use JWT-based authentication.
- Credentials are loaded through environment variables.
- Private credentials must never be committed to GitHub.

## 11. Limitations

- The application requires database connectivity.
- The authentication and Flask services must be available for their respective features.
- The current implementation is intended as an academic project and may require additional security, deployment, and scalability work before production use.

## 12. Future Enhancements

- Monthly budgets and spending limits
- Recurring expense support
- Export reports to CSV or PDF
- Budget alerts and savings goals
- Improved mobile-friendly interface
- More comprehensive automated testing
- Automated deployment

## 13. Conclusion

The Personal Expense Tracker demonstrates how Python, Streamlit, Flask, Node.js, and MySQL can be combined to build an expense management application. It integrates authentication, expense CRUD operations, validation, database storage, and data analysis in one project.
