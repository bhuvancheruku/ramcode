import streamlit as st
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

# Function to fetch data from the database
@st.cache(allow_output_mutation=True)
def fetch_data(user):
    font = "<font size='3' color='black'>"
    output = ""
    # Simulate data fetching from the database
    # Replace this with your actual data fetching logic
    rows = [("username", "amount", "type", "date", "balance")]  # Example data
    for row in rows:
        output += f"<tr><td>{font}{str(row[0])}</font></td>"
        output += f"<td>{font}{str(row[1])}</font></td>"
        output += f"<td>{font}{str(row[2])}</font></td>"
        output += f"<td>{font}{str(row[3])}</font></td>"
        output += f"<td>{font}{str(row[4])}</font></td>"
    return output

def login_action():
    global uname
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    data = st.file_uploader("Upload Fingerprint Image", type=["png"])
    index = 0
    # Simulate user data fetching from the database
    # Replace this with your actual user authentication logic
    users = [("username", "password")]  # Example data
    for row in users:
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
    # Simulate data fetching from the database
    # Replace this with your actual data fetching logic
    rows = [("username", "amount")]  # Example data
    for row in rows:
        if row[0] == user:
            amount = float(row[1])
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
        # Simulate update transaction in the database
        # Replace this with your actual update logic
        status = "Withdrawal Transaction Successful"
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
        # Simulate insert transaction in the database
        # Replace this with your actual insert logic
        status = "Transaction Successful"
    elif total > 0:
        total = total + float(amount)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Simulate update transaction in the database
        # Replace this with your actual update logic
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
    # Simulate user data fetching from the database
    # Replace this with your actual user check logic
    users = [("username")]  # Example data
    for row in users:
        if row[0] == user:
            status = user + " Username already exists"
            break
    if status == 'none':
        # Simulate insert user in the database
        # Replace this with your actual insert logic
        status = 'Signup process completed'
    st.success(status)

def logout():
    st.write("Logout Page")

# Streamlit app
def main():
    page = st.sidebar.selectbox("Choose a page", ["Home", "Login", "Signup", "Deposit", "Withdraw", "View Balance", "Logout"])

    if page == "Home":
        index()
    elif page == "Login":
        login()
        login_action()
    elif page == "Signup":
        signup()
        signup_action()
    elif page == "Deposit":
        deposit()
        deposit_action()
    elif page == "Withdraw":
        withdraw()
        withdraw_action()
    elif page == "View Balance":
        view_balance()
    elif page == "Logout":
        logout()

if __name__ == "__main__":
    main()
