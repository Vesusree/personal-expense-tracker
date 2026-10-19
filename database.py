
import os
import streamlit as st
import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        secrets = st.secrets

        connection = mysql.connector.connect(
            host=secrets.get("DB_HOST", os.getenv("DB_HOST", "localhost")),
            user=secrets.get("DB_USER", os.getenv("DB_USER", "root")),
            password=secrets.get("DB_PASSWORD", os.getenv("DB_PASSWORD", "")),
            database=secrets.get("DB_NAME", os.getenv("DB_NAME", "expense_tracker")),
            port=int(secrets.get("DB_PORT", os.getenv("DB_PORT", "3306"))),
            ssl_disabled=False
        )
        return connection

    except (Error, ValueError, KeyError) as error:
        print("Database connection failed:", error)
        return None
