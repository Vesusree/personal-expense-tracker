
import os
from datetime import date
from decimal import Decimal, InvalidOperation
from functools import wraps

import jwt
from flask import Flask, jsonify, request, g
from dotenv import load_dotenv

from database import get_connection

load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), "auth-server", ".env"))

app = Flask(__name__)
JWT_SECRET = os.getenv("JWT_SECRET")


def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not JWT_SECRET:
            return jsonify({"error": "Authentication is not configured"}), 500

        header = request.headers.get("Authorization", "")
        parts = header.split()

        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({"error": "Bearer token required"}), 401

        try:
            payload = jwt.decode(
                parts[1],
                JWT_SECRET,
                algorithms=["HS256"]
            )
            user_id = int(payload["id"])
            if user_id <= 0:
                raise ValueError("Invalid user ID")
            g.user_id = user_id
        except (jwt.InvalidTokenError, KeyError, TypeError, ValueError):
            return jsonify({"error": "Invalid or expired token"}), 401

        return func(*args, **kwargs)

    return wrapper


def get_categories(cursor):
    cursor.execute("SELECT category_id FROM categories")
    return {int(row[0]) for row in cursor.fetchall()}


@app.route("/api/categories", methods=["GET"])
def list_categories():
    connection = get_connection()

    if connection is None:
        return jsonify({"error": "Database unavailable"}), 503

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT category_id, category_name FROM categories ORDER BY category_name"
        )
        rows = cursor.fetchall()

        categories = [
            {
                "category_id": int(row[0]),
                "category_name": row[1]
            }
            for row in rows
        ]

        cursor.close()
        return jsonify(categories)

    except Exception:
        app.logger.exception("Failed to retrieve categories")
        return jsonify({"error": "Could not retrieve categories"}), 500

    finally:
        connection.close()

def read_expense_input(data, partial=False):
    if not isinstance(data, dict):
        raise ValueError("JSON object required")

    result = {}

    if not partial or "expense_date" in data:
        try:
            result["expense_date"] = date.fromisoformat(
                str(data["expense_date"])
            )
        except (KeyError, TypeError, ValueError):
            raise ValueError("expense_date must use YYYY-MM-DD")

    if not partial or "category_id" in data:
        try:
            result["category_id"] = int(data["category_id"])
        except (KeyError, TypeError, ValueError):
            raise ValueError("category_id must be an integer")

    if not partial or "amount" in data:
        try:
            amount = Decimal(str(data["amount"]))
        except (KeyError, TypeError, InvalidOperation, ValueError):
            raise ValueError("amount must be a valid number")

        if not amount.is_finite() or amount <= 0 or amount > Decimal("99999999.99"):
            raise ValueError("amount must be greater than zero and within the database limit")

        result["amount"] = amount

    for field in ("description", "payment_method"):
        if not partial or field in data:
            value = data.get(field)
            if value is not None and not isinstance(value, str):
                raise ValueError(f"{field} must be text")
            if field == "description" and value and len(value) > 255:
                raise ValueError("description must be at most 255 characters")
            if field == "payment_method" and value and len(value) > 50:
                raise ValueError("payment_method must be at most 50 characters")
            result[field] = value

    return result



def expense_dict(row):
    return {
        "expense_id": int(row[0]),
        "expense_date": row[1].isoformat() if row[1] else None,
        "category_id": int(row[2]),
        "category_name": row[3],
        "amount": float(row[4]),
        "description": row[5],
        "payment_method": row[6],
    }


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Personal Expense Tracker Flask API",
        "status": "running"
    })


@app.route("/health", methods=["GET"])
def health():
    connection = get_connection()
    if connection is None:
        return jsonify({"status": "error", "database": "disconnected"}), 503

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception:
        app.logger.exception("Database health check failed")
        return jsonify({"status": "error", "database": "disconnected"}), 503
    finally:
        connection.close()


@app.route("/api/expenses", methods=["GET"])
@require_auth
def list_expenses():
    connection = get_connection()
    if connection is None:
        return jsonify({"error": "Database unavailable"}), 503

    try:
        cursor = connection.cursor()
        cursor.execute(
            """SELECT e.expense_id, e.expense_date, e.category_id,
          c.category_name, e.amount, e.description,
          e.payment_method
   FROM expenses e
   JOIN categories c ON e.category_id = c.category_id
   WHERE e.user_id = %s
   ORDER BY e.expense_date DESC, e.expense_id DESC""",
            (g.user_id,)
        )
        rows = cursor.fetchall()
        return jsonify([expense_dict(row) for row in rows])
    except Exception:
        app.logger.exception("Failed to list expenses")
        return jsonify({"error": "Could not retrieve expenses"}), 500
    finally:
        connection.close()


@app.route("/api/expenses", methods=["POST"])
@require_auth
def create_expense():
    try:
        data = read_expense_input(request.get_json(silent=True))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    connection = get_connection()
    if connection is None:
        return jsonify({"error": "Database unavailable"}), 503

    try:
        cursor = connection.cursor()
        if data["category_id"] not in get_categories(cursor):
            return jsonify({"error": "Unknown category_id"}), 400

        cursor.execute(
            """INSERT INTO expenses
               (expense_date, category_id, amount, description,
                payment_method, user_id)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                data["expense_date"], data["category_id"], data["amount"],
                data["description"], data["payment_method"], g.user_id
            )
        )
        new_id = cursor.lastrowid
        connection.commit()
        return jsonify({"message": "Expense created", "expense_id": new_id}), 201
    except Exception:
        connection.rollback()
        app.logger.exception("Failed to create expense")
        return jsonify({"error": "Could not create expense"}), 500
    finally:
        connection.close()


@app.route("/api/expenses/<int:expense_id>", methods=["PUT"])
@require_auth
def update_expense(expense_id):
    try:
        data = read_expense_input(request.get_json(silent=True), partial=True)
        if not data:
            return jsonify({"error": "At least one field is required"}), 400
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    connection = get_connection()
    if connection is None:
        return jsonify({"error": "Database unavailable"}), 503

    try:
        cursor = connection.cursor()
        if "category_id" in data and data["category_id"] not in get_categories(cursor):
            return jsonify({"error": "Unknown category_id"}), 400

        allowed = {"expense_date", "category_id", "amount", "description", "payment_method"}
        fields = [field for field in data if field in allowed]
        assignments = ", ".join(f"{field} = %s" for field in fields)
        values = [data[field] for field in fields]

        cursor.execute(
            f"""UPDATE expenses SET {assignments}
                WHERE expense_id = %s AND user_id = %s""",
            (*values, expense_id, g.user_id)
        )
        if cursor.rowcount == 0:
            connection.rollback()
            cursor.execute(
                "SELECT expense_id FROM expenses WHERE expense_id = %s AND user_id = %s",
                (expense_id, g.user_id)
            )
            exists = cursor.fetchone()
            if not exists:
                return jsonify({"error": "Expense not found"}), 404

        connection.commit()
        return jsonify({"message": "Expense updated"})
    except Exception:
        connection.rollback()
        app.logger.exception("Failed to update expense")
        return jsonify({"error": "Could not update expense"}), 500
    finally:
        connection.close()


@app.route("/api/expenses/<int:expense_id>", methods=["DELETE"])
@require_auth
def delete_expense(expense_id):
    connection = get_connection()
    if connection is None:
        return jsonify({"error": "Database unavailable"}), 503

    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM expenses WHERE expense_id = %s AND user_id = %s",
            (expense_id, g.user_id)
        )
        if cursor.rowcount == 0:
            return jsonify({"error": "Expense not found"}), 404

        connection.commit()
        return jsonify({"message": "Expense deleted"})
    except Exception:
        connection.rollback()
        app.logger.exception("Failed to delete expense")
        return jsonify({"error": "Could not delete expense"}), 500
    finally:
        connection.close()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
