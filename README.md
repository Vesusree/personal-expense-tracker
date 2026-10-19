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

- Python and Streamlit
- Pandas, NumPy, and Matplotlib
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
- A configured MySQL database with the required tables
- A configured email account for verification messages

## Configuration

Create a `.env` file in the project root for the Python database connection. Create another `.env` file inside `auth-server/` for the authentication server.

Use the environment-variable names expected by `database.py` and `auth-server/server.js`.

**Never commit `.env` files or real credentials to GitHub.**

## Run the Application on Windows

### 1. Open a terminal in the project root

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```powershell
pip install -r requirements.txt
```

### 2. Start the authentication server

Open a terminal in the project root and run:

```powershell
cd auth-server
npm install
node server.js
```

Keep this terminal open.

### 3. Start the Streamlit application

Open a second terminal in the project root, activate the virtual environment if necessary, and run:

```powershell
python -m streamlit run main.py
```

Open the local URL displayed in the terminal.

## Security Notes

- Passwords are stored as hashes.
- Email verification is required before login.
- Expense queries are scoped to the logged-in user.
- Credentials are loaded through environment variables.
- Configure secure credentials before public deployment.

## Future Improvements

- Cloud deployment
- Budget limits and spending alerts
- Improved mobile-friendly interface
- Automated testing and deployment

