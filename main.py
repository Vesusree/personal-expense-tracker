
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from database import get_connection
import requests
from urllib.parse import urljoin
from datetime import date, timedelta


def get_logged_in_user_id():
    user = st.session_state.get("auth_user")
    if not user:
        return None

    return user.get("id")

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# ---------- AUTHENTICATION ----------

AUTH_API_URL = "http://localhost:3000"


if "auth_token" not in st.session_state:
    st.session_state.auth_token = None

if "auth_user" not in st.session_state:
    st.session_state.auth_user = None


if not st.session_state.auth_token:
    st.title("🔐 Welcome to Personal Expense Tracker")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        st.subheader("Login to your account")

        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input(
            "Password", type="password", key="login_password"
        )

        if st.button("Login", key="login_button"):
            try:
                response = requests.post(
                    f"{AUTH_API_URL}/login",
                    json={
                        "email": login_email,
                        "password": login_password,
                    },
                    timeout=15,
                )

                if response.status_code == 200:
                    result = response.json()
                    st.session_state.auth_token = result["token"]
                    st.session_state.auth_user = result["user"]
                    st.rerun()
                else:
                    st.error(response.json().get("message", "Login failed."))

            except requests.RequestException:
                st.error(
                    "Cannot connect to the authentication server. "
                    "Make sure the Node.js server is running."
                )

    with register_tab:
        st.subheader("Create an account")

        register_name = st.text_input("Name", key="register_name")
        register_email = st.text_input("Email", key="register_email")
        register_password = st.text_input(
            "Password (at least 8 characters)",
            type="password",
            key="register_password",
        )

        if st.button("Register", key="register_button"):
            try:
                response = requests.post(
                    f"{AUTH_API_URL}/register",
                    json={
                        "name": register_name,
                        "email": register_email,
                        "password": register_password,
                    },
                    timeout=20,
                )

                if response.status_code == 201:
                    st.success(response.json().get("message"))
                    st.info("Check your email and verify your account before logging in.")
                else:
                    st.error(response.json().get("message", "Registration failed."))

            except requests.RequestException:
                st.error(
                    "Cannot connect to the authentication server. "
                    "Make sure the Node.js server is running."
                )

    st.stop()

st.success(f"Logged in as {st.session_state.auth_user['name']}")

if st.button("Logout"):
    st.session_state.auth_token = None
    st.session_state.auth_user = None
    st.rerun()

# ---------- END AUTHENTICATION ----------


st.title("💰 Personal Expense Tracker")
st.caption("Manage your expenses, understand your spending, and plan better.")

# ---------- DATABASE HELPERS ----------

def fetch_data(query, params=None):
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        rows = cursor.fetchall()
        return pd.DataFrame(rows)
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()
    finally:
        cursor.close()
        conn.close()


def execute_query(query, params=None):
    conn = get_connection()
    if conn is None:
        st.error("Could not connect to MySQL.")
        return False

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        st.error(f"Database error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        conn.close()


def get_categories():
    df = fetch_data(
        "SELECT category_id, category_name "
        "FROM categories ORDER BY category_name"
    )
    return df



def get_expenses():
    user_id = get_logged_in_user_id()

    if user_id is None:
        return pd.DataFrame()

    return fetch_data(
        """
        SELECT e.expense_id, e.expense_date,
               c.category_name, e.category_id,
               e.amount, e.description, e.payment_method
        FROM expenses e
        JOIN categories c ON e.category_id = c.category_id
        WHERE e.user_id = %s
        ORDER BY e.expense_date DESC, e.expense_id DESC
        """,
        (user_id,)
    )



# ---------- LOAD DATA ----------

categories = get_categories()

if categories.empty:
    st.error(
        "No categories found. Please check your MySQL database "
        "and make sure the default categories were inserted."
    )
    st.stop()

category_names = categories["category_name"].tolist()
category_ids = dict(
    zip(categories["category_name"], categories["category_id"])
)

# ---------- SIDEBAR ----------

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a page",
    [
        "Dashboard",
        "Add Expense",
        "Manage Expenses",
        "Reports & Analysis"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Your expenses are stored in your local MySQL database.")

# ---------- DASHBOARD ----------

if page == "Dashboard":
    st.header("📊 Spending Dashboard")

    expenses = get_expenses()

    if expenses.empty:
        st.info("No expenses recorded yet. Go to Add Expense to get started.")
    else:
        expenses["expense_date"] = pd.to_datetime(expenses["expense_date"])
        expenses["amount"] = pd.to_numeric(expenses["amount"])

        today = date.today()
        month_start = today.replace(day=1)

        this_month = expenses[
            (expenses["expense_date"].dt.date >= month_start) &
            (expenses["expense_date"].dt.date <= today)
        ]

        total_spent = float(this_month["amount"].sum())
        total_records = len(this_month)

        if not this_month.empty:
            monthly_category = this_month.groupby(
                "category_name"
            )["amount"].sum()
            highest_category = monthly_category.idxmax()
            highest_amount = float(monthly_category.max())
        else:
            highest_category = "No expenses"
            highest_amount = 0.0

        all_time_total = float(expenses["amount"].sum())

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Spent This Month", f"₹{total_spent:,.2f}")
        col2.metric("Expenses This Month", total_records)
        col3.metric("Highest Category", highest_category)
        col4.metric("All-Time Spending", f"₹{all_time_total:,.2f}")

        st.divider()
        left, right = st.columns(2)

        with left:
            st.subheader("This Month: Category Breakdown")
            if not this_month.empty:
                category_totals = this_month.groupby(
                    "category_name"
                )["amount"].sum().sort_values(ascending=False)

                fig, ax = plt.subplots()
                ax.pie(
                    category_totals.values,
                    labels=category_totals.index,
                    autopct="%1.1f%%",
                    startangle=90
                )
                ax.axis("equal")
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.info("No expenses recorded this month.")

        with right:
            st.subheader("Monthly Spending Trend")
            monthly = expenses.copy()
            monthly["month"] = (
                monthly["expense_date"].dt.to_period("M").astype(str)
            )
            monthly_totals = monthly.groupby(
                "month"
            )["amount"].sum().sort_index().tail(12)

            fig, ax = plt.subplots()
            monthly_totals.plot(kind="bar", ax=ax)
            ax.set_xlabel("Month")
            ax.set_ylabel("Amount (₹)")
            ax.set_title("Last 12 Months with Recorded Expenses")
            plt.xticks(rotation=45, ha="right")
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        st.subheader("Recent Expenses")
        st.dataframe(
            expenses[
                [
                    "expense_date", "category_name", "amount",
                    "description", "payment_method"
                ]
            ].head(10),
            width="stretch",
            hide_index=True
        )

# ---------- ADD EXPENSE ----------

elif page == "Add Expense":
    st.header("➕ Add a New Expense")

    with st.form("add_expense_form", clear_on_submit=True):
        expense_date = st.date_input("Expense Date", value=date.today())
        category = st.selectbox("Category", category_names)
        amount = st.number_input(
            "Amount (₹)", min_value=0.01, value=100.00, step=10.00
        )
        description = st.text_input(
            "Description", placeholder="e.g. Lunch with friends"
        )
        payment_method = st.selectbox(
            "Payment Method",
            ["Cash", "UPI", "Debit Card", "Credit Card", "Net Banking", "Other"]
        )

        submitted = st.form_submit_button(
            "Save Expense", type="primary", width="stretch"
        )

       
        if submitted:
            user_id = get_logged_in_user_id()

            if user_id is None:
                st.error("Please log in before adding an expense.")
                st.stop()

            success = execute_query(
                """
                INSERT INTO expenses
                    (expense_date, category_id, amount,
                     description, payment_method, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    expense_date,
                    category_ids[category],
                    round(amount, 2),
                    description.strip(),
                    payment_method,
                    user_id
                )
            )

            if success:
                st.success("Expense saved successfully!")
                st.rerun()


# ---------- MANAGE EXPENSES ----------

elif page == "Manage Expenses":
    st.header("📝 Manage Expenses")

    expenses = get_expenses()

    if expenses.empty:
        st.info("There are no expenses to manage yet.")
    else:
        expenses["expense_date"] = pd.to_datetime(
            expenses["expense_date"]
        ).dt.date

        st.subheader("All Expense Records")
        st.dataframe(
            expenses[
                [
                    "expense_id", "expense_date", "category_name",
                    "amount", "description", "payment_method"
                ]
            ],
            width="stretch",
            hide_index=True
        )

        st.divider()
        st.subheader("Edit an Expense")

        expense_ids = expenses["expense_id"].astype(int).tolist()
        selected_id = st.selectbox("Select Expense ID to Edit", expense_ids)

        selected = expenses[
            expenses["expense_id"] == selected_id
        ].iloc[0]

        current_category = selected["category_name"]
        current_payment = selected["payment_method"]
        payment_options = [
            "Cash", "UPI", "Debit Card", "Credit Card",
            "Net Banking", "Other"
        ]

        if current_payment not in payment_options:
            payment_options.append(current_payment)

        with st.form("edit_expense_form"):
            new_date = st.date_input(
                "Date", value=selected["expense_date"], key="edit_date"
            )
            new_category = st.selectbox(
                "Category",
                category_names,
                index=category_names.index(current_category)
            )
            new_amount = st.number_input(
                "Amount (₹)",
                min_value=0.01,
                value=float(selected["amount"]),
                step=10.00,
                key="edit_amount"
            )
            new_description = st.text_input(
                "Description",
                value=(
                    "" if pd.isna(selected["description"])
                    else str(selected["description"])
                ),
                key="edit_description"
            )
            new_payment = st.selectbox(
                "Payment Method",
                payment_options,
                index=payment_options.index(current_payment)
                if current_payment in payment_options else 0
            )

            update_clicked = st.form_submit_button(
                "Update Expense", type="primary"
            )

            if update_clicked:
                user_id = get_logged_in_user_id()

                if user_id is None:
                    st.error("Please log in before editing an expense.")
                    st.stop()

                success = execute_query(
                    """
                    UPDATE expenses
                    SET expense_date=%s, category_id=%s, amount=%s,
                        description=%s, payment_method=%s
                    WHERE expense_id=%s AND user_id=%s
                    """,
                    (
                        new_date,
                        category_ids[new_category],
                        round(new_amount, 2),
                        new_description.strip(),
                        new_payment,
                        selected_id,
                        user_id
                    )
                )

                if success:
                    st.success("Expense updated successfully!")
                    st.rerun()

        st.divider()
        st.subheader("Delete an Expense")
        st.warning("Deleting an expense permanently removes it from the database.")

        confirm_delete = st.checkbox(
            f"I want to delete expense ID {selected_id}",
            key="confirm_delete"
        )

        if st.button("Delete Selected Expense", type="secondary"):
            if confirm_delete:
                user_id = get_logged_in_user_id()

                if user_id is None:
                    st.error("Please log in before deleting an expense.")
                    st.stop()

                success = execute_query(
                    """
                    DELETE FROM expenses
                    WHERE expense_id = %s AND user_id = %s
                    """,
                    (int(selected_id), user_id)
                )

                if success:
                    st.success("Expense deleted successfully!")
                    st.rerun()
            else:
                st.error("Please confirm deletion using the checkbox.")


# ---------- REPORTS & ANALYSIS ----------

elif page == "Reports & Analysis":
    st.header("📈 Reports & Expense Analysis")

    expenses = get_expenses()

    if expenses.empty:
        st.info("Add expenses first to generate reports.")
    else:
        expenses["expense_date"] = pd.to_datetime(
            expenses["expense_date"]
        )
        expenses["amount"] = pd.to_numeric(expenses["amount"])

        min_date = expenses["expense_date"].min().date()
        max_date = expenses["expense_date"].max().date()

        st.subheader("Filter Your Report")

        c1, c2 = st.columns(2)
        with c1:
            start_date = st.date_input(
                "Start Date",
                value=min_date,
                min_value=min_date,
                max_value=max_date
            )
        with c2:
            end_date = st.date_input(
                "End Date",
                value=max_date,
                min_value=min_date,
                max_value=max_date
            )

        filter_categories = st.multiselect(
            "Categories",
            category_names,
            default=category_names
        )

        if start_date > end_date:
            st.error("Start date must be on or before end date.")
            st.stop()

        filtered = expenses[
            (expenses["expense_date"].dt.date >= start_date) &
            (expenses["expense_date"].dt.date <= end_date) &
            (expenses["category_name"].isin(filter_categories))
        ].copy()

        total = float(filtered["amount"].sum())
        count = len(filtered)
        average = float(np.mean(filtered["amount"])) if count else 0.0

        m1, m2, m3 = st.columns(3)
        m1.metric("Filtered Total", f"₹{total:,.2f}")
        m2.metric("Number of Expenses", count)
        m3.metric("Average Expense", f"₹{average:,.2f}")

        st.subheader("Category-Wise Breakdown")

        if not filtered.empty:
            category_summary = filtered.groupby(
                "category_name"
            )["amount"].sum().sort_values(ascending=False)

            summary_df = category_summary.rename(
                "Total Spent (₹)"
            ).reset_index()

            summary_df["Share (%)"] = (
                summary_df["Total Spent (₹)"] / total * 100
                if total > 0 else 0
            ).round(2)

            st.dataframe(
                summary_df,
                width="stretch",
                hide_index=True
            )

            st.write(
                "**Highest-Spending Category:**",
                category_summary.idxmax()
            )

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Category Pie Chart")
                fig, ax = plt.subplots()
                ax.pie(
                    category_summary.values,
                    labels=category_summary.index,
                    autopct="%1.1f%%",
                    startangle=90
                )
                ax.axis("equal")
                st.pyplot(fig)
                plt.close(fig)

            with col2:
                st.subheader("Category Bar Chart")
                fig, ax = plt.subplots()
                category_summary.plot(kind="bar", ax=ax)
                ax.set_xlabel("Category")
                ax.set_ylabel("Amount (₹)")
                plt.xticks(rotation=45, ha="right")
                fig.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

            st.subheader("Month-Wise Spending")

            monthly = filtered.copy()
            monthly["month"] = (
                monthly["expense_date"].dt.to_period("M").astype(str)
            )
            monthly_summary = monthly.groupby(
                "month"
            )["amount"].sum().sort_index()

            fig, ax = plt.subplots()
            monthly_summary.plot(kind="bar", ax=ax)
            ax.set_xlabel("Month")
            ax.set_ylabel("Amount (₹)")
            plt.xticks(rotation=45, ha="right")
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

            st.subheader("Filtered Expense Records")
            st.dataframe(
                filtered[
                    [
                        "expense_id", "expense_date", "category_name",
                        "amount", "description", "payment_method"
                    ]
                ],
                width="stretch",
                hide_index=True
            )

            csv_data = filtered.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Report as CSV",
                data=csv_data,
                file_name="expense_report.csv",
                mime="text/csv"
            )

        else:
            st.info("No expenses match the selected filters.")

st.sidebar.divider()
st.sidebar.caption("Personal Expense Tracker | Python + MySQL")
