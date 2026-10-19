# Personal Expense Tracker

A Python-based expense tracking application that helps users record, manage, and analyze personal spending.

## Features

- User registration and email verification
- Secure login with hashed passwords
- Add, view, edit, and delete expenses
- User-specific expense records
- Expense summaries and visualizations
- Reports and CSV export
- MySQL database integration

## Technologies Used

- Python
- Streamlit
- Pandas and NumPy
- Matplotlib
- MySQL
- Node.js and Express
- JWT authentication
- bcrypt password hashing
- Nodemailer for email verification

## Project Structure

```text
personal-expense-tracker/
├── auth-server/
│   ├── server.js
│   ├── package.json
│   ├── package-lock.json
│   └── ca.pem
├── main.py
├── database.py
├── requirements.txt
├── schema.sql
└── README.md
```

## Prerequisites

- Python 3
- Node.js and npm
- A MySQL database with the required tables
- Email account configured for sending verification emails

## Configuration

Create a `.env` file in the project root for the Python database connection. Create another `.env` file inside `auth-server/` for the authentication service.

Use the variable names expected by `database.py` and `auth-server/server.js`. Keep all real credentials private. Never commit `.env` files to GitHub.

## Run the Application

### 1. Install Python dependencies

```bash
python -m venv .venv
```

Activate the virtual environment, then run:

```bash
pip install -r requirements.txt
```

### 2. Start the authentication server

In a terminal:

```bash
cd auth-server
npm install
node server.js
```

Keep this terminal open.

### 3. Start the Streamlit application

Open a second terminal in the project root and run:

```bash
python -m streamlit run main.py
```

Open the local URL shown in the terminal.

## Security Notes

- Passwords are stored as hashes.
- Email verification is required before login.
- Expense queries are scoped to the logged-in user.
- Credentials must be provided through environment variables.
- Configure fresh credentials before deploying to a public server.

## Future Improvements

- Cloud deployment
- Budget limits and spending alerts
- Improved mobile-friendly interface
- Automated testing and deployment
