import os
import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv(
                "DB_HOST",
                "mysql-db01f0e-vesusreepilliboyana-db6b.i.aivencloud.com"
            ),
            user=os.getenv("DB_USER", "avnadmin"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "defaultdb"),
            port=int(os.getenv("DB_PORT", "25805")),
            ssl_disabled=False
        )
        return connection

    except (Error, ValueError) as error:
        print("Database connection failed:", error)
        return None
