
import os
import mysql.connector
import streamlit as st
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


def get_db_setting(key, default=None):
    value = os.getenv(key)

    if value:
        return value

    try:
        return st.secrets.get(key, default)
    except Exception:
        return default


def get_connection():
    try:
        host = get_db_setting("DB_HOST")
        user = get_db_setting("DB_USER")
        password = get_db_setting("DB_PASSWORD")
        database = get_db_setting("DB_NAME", "defaultdb")
        port = int(get_db_setting("DB_PORT", "3306"))

        if not host or not user or not password:
            raise ValueError(
                "Missing required database settings."
            )

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            ssl_ca=os.path.join(
                os.path.dirname(__file__),
                "auth-server",
                "ca.pem"
            ),
            ssl_verify_cert=True,
            connection_timeout=15
        )

  
        return connection

    except Exception as error:
        print("Database connection failed:", repr(error))
        try:
            import streamlit as st
            st.error(f"MySQL connection failed: {error}")
        except Exception:
            pass
        return None


