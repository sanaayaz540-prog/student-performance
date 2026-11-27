
import streamlit as st
import pandas as pd
import pyodbc
import bcrypt

st.title("Student Performance Dashboard")

# Database connection
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=.\\SQLEXPRESS;"
    "DATABASE=studentperformance;"
    "Trusted_Connection=yes;"
)

# Login session
if "login" not in st.session_state:
    st.session_state.login = False

if "username" not in st.session_state:
    st.session_state.username = ""

# Login and Signup
if not st.session_state.login:

    choice = st.selectbox("Choose", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button(choice):

        if username == "" or password == "":
            st.warning("Enter username and password.")

        else:
            conn = pyodbc.connect(conn_str)
            cur = conn.cursor()

            if choice == "Signup":

                cur.execute(
                    "SELECT username FROM Users WHERE username = ?",
                    (username,)
                )

                result = cur.fetchone()

                if result:
                    st.error("Username already exists.")

                else:
                    hashed = bcrypt.hashpw(
                        password.encode(), bcrypt.gensalt()
                    ).decode()

                    cur.execute(
                        "INSERT INTO Users (username, password_hash) VALUES (?, ?)",
                        (username, hashed)
                    )

                    conn.commit()
                    st.success("Account created!")

            else:

                cur.execute(
                    "SELECT password_hash FROM Users WHERE username = ?",
                    (username,)
                )

                result = cur.fetchone()

                if result and bcrypt.checkpw(
                    password.encode(), result[0].encode()
                ):
                    st.session_state.login = True
                    st.session_state.username = username
                    st.rerun()

                else:
                    st.error("Invalid username or password.")

            conn.close()

# Dashboard
else:

    st.write("Welcome", st.session_state.username)

    if st.button("Logout"):
        st.session_state.login = False
        st.session_state.username = ""
        st.rerun()

    # Read dataset
    df = pd.read_csv("StudentPerformanceFactors.csv")

    st.subheader("Dataset Preview")

    st.write("Total Rows:", len(df))
    st.write("Total Columns:", len(df.columns))

    st.dataframe(df.head(15))

    # Visualization
    st.subheader("Visualization")

    columns = df.select_dtypes(include="number").columns

    selected = st.selectbox("Select Column", columns)

    st.bar_chart(df[selected].head(25))
