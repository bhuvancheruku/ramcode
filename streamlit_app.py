import streamlit as st
import mysql.connector
from datetime import datetime

st.set_page_config(page_title='ATM Application', page_icon=':bank:')

global uname

def deposit():
    output = f"Username: {uname}"
    st.write(output)

def withdraw():
    output = f"Username: {uname}"
    st.write(output)

def index():
    st.write("Welcome to the ATM Application")

def login():
    st.write("Login Page")

def signup():
    st.write("Signup Page")

def view_balance():
    font = "<font size='3' color='black'>"
    output = ""
    con = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='', database='atm')
    with con:
        cur = con.cursor()
        cur.execute(f"select * FROM transaction where username='{uname}'")
        rows = cur.fetchall()
        for row in rows:
            output += f"<tr><td>{font}{str(row[0])}</font></td>"
            output += f"<td>{font}{str(row[1])}</font></td>"
            output += f"<td>{font}{str(row[2])}</font></td>"
            output += f"<td>{font}{str(row[3])}</font></td>"
            output += f"<td>{font}{str(row[4])}</font></td>"
    st.write(output)

def login_action():
    global uname
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    data = st.file_uploader("Upload Fingerprint Image", type=["png"])
    index = 0
    con = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='', database='atm')
    with con:
        cur = con.cursor()
        cur.execute("select * FROM users")
        rows = cur.fetchall()
        for row in rows:
            if row[0] == user and password == row[1]:
                in_file = open(f"C:/Users/marut/OneDrive/Desktop/FingerprintATM/static/users/{user}.png", "rb")
                avail_data = in_file.read()
                in_file.close()
                if avail_data == data:
                    index = 1
                    uname = user
                    break
    if index == 0:
        st.warning("Invalid login details")
    else:
        st.success(f"Welcome {uname}")

def get_amount(user):
    amount = 0
    con = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='', database='atm')
    with con:
        cur = con.cursor()
        cur.execute("select * FROM transaction")
        rows = cur.fetchall()
        for row in rows:
            if row[0] == user:
                amount = float(row[4])
                break
    return amount

def withdraw_action():
    user = st.text_input("Username")
    amount = st.text_input("Amount", type="number")
    total = get_amount(user)
    withdraw = float(amount)
    status = "Error in depositing amount"
    if total > withdraw:
        total = total - withdraw
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        student_sql_query = f"update transaction set transaction_amount='{amount}',transaction_type='Withdrawl',transaction_date='{timestamp}',total_balance='{total}' where username='{user}'"
        db_connection = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='', database='atm')
        db_cursor = db_connection.cursor()
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            status = "Withdrawl Transaction Successful"
    else:
        status = "Insufficient Fund"
    st.success(status)

def deposit_action():
    user = st.text_input("Username")
    amount = st.text_input("Amount", type="number")
    total = get_amount(user)
    status = "Error in depositing amount"
    if total == 0:
        total = total + float(amount)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        student_sql_query = f"INSERT INTO transaction(username,transaction_amount,transaction_type,transaction_date,total_balance) VALUES('{user}','{amount}','Deposit','{timestamp}','{total}')"
        db_connection = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='', database='atm')
        db_cursor = db_connection.cursor()
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            status = "Transaction Successful"
    elif total > 0:
        total = total + float(amount)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        student_sql_query = f"update transaction set transaction_amount='{amount}',transaction_type='Deposit',transaction_date='{timestamp}',total_balance='{total}' where username='{user}'"
        db_connection = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='', database='atm')
        db_cursor = db_connection.cursor()
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            status = "Transaction Successful"
    st.success(status)

def signup_action():
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    address = st.text_input("Address")
    gender = st.radio("Gender", ["Male", "Female", "Other"])
    data = st.file_uploader("Upload Fingerprint Image", type=["png"])
    status = "none"
    con = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='', database='atm')
    with con:
        cur = con.cursor()
        cur.execute("select * FROM users")
        rows = cur.fetchall()
        for row in rows:
            if row[0] == user:
                status = user + " Username already exists"
                break
    if status == 'none':
        db_connection = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='', database='atm')
        db_cursor = db_connection.cursor()
        student_sql_query = f"INSERT INTO users(username,password,contact_no,emailid,address,gender) VALUES('{user}','{password}','{phone}','{email}','{address}','{gender}')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        if db_cursor.rowcount == 1:
            out_file = open(f"C:/Users/marut/OneDrive/Desktop/FingerprintATM/static/users/{user}.png", "wb")
            out_file.write(data)
            out_file.close()
            status = 'Signup process completed'
    st.success(status)

def logout():
    st.write("Logout Page")
