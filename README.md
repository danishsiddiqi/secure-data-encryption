# 🔐 Secure Data Storage System with Encryption (Streamlit + Fernet)

This is a simple yet secure data encryption and decryption app built using **Python**, **Streamlit**, and **Fernet (from cryptography)**. It allows users to store and retrieve confidential text data using a secure passkey and persistent encryption.

---

## 📦 Features

- 🔒 Data encryption using Fernet symmetric encryption
- 🔑 Passkey protected access (SHA-256 hashed)
- 🧠 In-memory + file-based storage (`data.json`)
- 🗝️ Persistent encryption key (`fernet.key`)
- 🚫 Lockout after multiple failed attempts
- 👤 Basic login functionality for reauthorization
- 📄 Built-in Streamlit UI for storing and retrieving text

---

## 🛠️ Technologies & Libraries Used

```bash
streamlit
cryptography
hashlib
os
json


You can install dependencies with:

pip install streamlit cryptography


🚀 How to Run the App

1.Clone this repository or download the files.

2.Open terminal in the project folder.

3.Run the Streamlit app.

🔐 Notes
The encryption key (fernet.key) must not be deleted or rotated unless you're prepared to lose access to previously stored encrypted data.

This project uses simple in-memory logic and data.json for learning/demo purposes. For production, consider using a secure database and authentication system.







