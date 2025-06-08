# 🛡️ Simple Password Manager (Python Project)

A beginner-friendly password manager built with Python. This project demonstrates basic concepts like encryption, file handling, database management, and user input for securely managing passwords on the command line.

> ⚠️ **DISCLAIMER**:  
> This password manager is a simple educational project and **not** intended for production or real-world use. If you need a secure, production-ready password manager, consider using trusted solutions like [KeePassXC](https://keepassxc.org/) or [Bitwarden](https://bitwarden.com/).

## 🚀 Features

- Add new password entries (service name, username, password)
- View saved credentials
- Delete entries
- Encrypt and decrypt password storage
- Command-line interface

## 🔐 Security

- Passwords are stored in an encrypted format using basic symmetric encryption (e.g., Fernet from `cryptography` library).
- A master password is used to unlock the manager and decrypt data.

> **Note:** This project is designed for learning purposes. It does not follow advanced security best practices such as key derivation functions (KDFs), secure vault storage, or tamper detection.

## 📦 Requirements

- Python 3.13+
- [`uv`](https://github.com/astral-sh/uv) package manager
- `cryptography` library

Install dependencies using `uv`:

```bash
uv run main.py
