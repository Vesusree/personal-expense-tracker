
import os
import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "expense_tracker"),
            port=int(os.getenv("DB_PORT", "3306"))
        )
        return connection

    except (Error, ValueError) as error:
        print("Database connection failed:", error)
        return None

