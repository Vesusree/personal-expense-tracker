
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "defaultdb"),
            port=int(os.getenv("DB_PORT", "3306")),
            ssl_ca=os.path.join(
                os.path.dirname(__file__),
                "auth-server",
                "ca.pem"
            ),
            ssl_verify_cert=True
        )
        return connection

    except (Error, ValueError) as error:
        print("Database connection failed:", error)
        return None
