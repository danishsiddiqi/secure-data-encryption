import streamlit as st
import hashlib
import os
from cryptography.fernet import Fernet
import json

# --- In-memory storage ---
# --- Constants ---
DATA_FILE = "data.json"

# --- Load/Save stored data to file ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# --- Initialize stored data ---
stored_data = load_data()

login_credentials = {"admin": "admin123"}  # Simple login
failed_attempts = {}

# --- Load or generate Fernet key ---
def load_or_generate_key():
    key_file = "fernet.key"
    if os.path.exists(key_file):
        with open(key_file, "rb") as file:
            return file.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, "wb") as file:
            file.write(key)
        return key

fernet_key = load_or_generate_key()
fernet = Fernet(fernet_key)

# --- Hashing passkey ---
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# --- Insert new data ---
def insert_data(username, text, passkey):
    hashed = hash_passkey(passkey)
    encrypted = fernet.encrypt(text.encode()).decode()
    stored_data[username] = {"encrypted_text": encrypted, "passkey": hashed}
    failed_attempts[username] = 0
    save_data(stored_data)

# --- Retrieve data ---
def retrieve_data(username, passkey):
    if username not in stored_data:
        return False, "No data found."

    if failed_attempts.get(username, 0) >= 3:
        return False, "Too many failed attempts. Please login."

    hashed_input = hash_passkey(passkey)
    if hashed_input == stored_data[username]["passkey"]:
        failed_attempts[username] = 0
        decrypted = fernet.decrypt(stored_data[username]["encrypted_text"].encode()).decode()
        return True, decrypted
    else:
        failed_attempts[username] = failed_attempts.get(username, 0) + 1
        return False, f"Incorrect passkey. Attempts: {failed_attempts[username]}"

# --- Simple login ---
def login(user, pwd):
    return login_credentials.get(user) == pwd

# --- Streamlit UI ---
st.title("🔐 Secure Data Storage System")

page = st.sidebar.selectbox("Navigate", ["Home", "Insert Data", "Retrieve Data", "Login Page"])

if page == "Home":
    st.subheader("Welcome!")
    st.info("Use the sidebar to insert or retrieve data securely.")

elif page == "Insert Data":
    st.subheader("📥 Store Your Data")
    user = st.text_input("Enter username")
    text = st.text_area("Enter text to store")
    passkey = st.text_input("Enter passkey", type="password")
    if st.button("Store Data"):
        if user and text and passkey:
            insert_data(user, text, passkey)
            st.success("✅ Data encrypted and stored securely!")
        else:
            st.error("Please fill all fields.")

elif page == "Retrieve Data":
    st.subheader("📤 Retrieve Your Data")
    user = st.text_input("Enter username")
    passkey = st.text_input("Enter your passkey", type="password")
    if st.button("Retrieve"):
        success, result = retrieve_data(user, passkey)
        if success:
            st.success("✅ Decryption Successful!")
            st.code(result)
        else:
            if "login" in result.lower():
                st.error(result)
                st.warning("Go to Login Page to reauthorize.")
            else:
                st.warning(result)

elif page == "Login Page":
    st.subheader("🔐 Reauthorization Required")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(user, pwd):
            st.success("✅ Login successful. Attempts reset.")
            failed_attempts[user] = 0
        else:
            st.error("❌ Invalid login.")
