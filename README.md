# Password-Manager
Description
YG's Password Manager is a secure, user-friendly password manager that stores and manages your passwords. With a superhero-themed interface, it offers multiple functionalities like adding, fetching, and checking password security. It uses SQLite for database storage and Argon2 for password hashing.

Features
Secure password storage using SQLite and Argon2
Password strength check
Password breach check using the Pwned Passwords API
Password and passphrase generation

Installation
Clone this repository:
git clone https://github.com/YeranG30/YGs-Password-Manager.git

Navigate into the project directory:

cd repository

Install the required packages:
pip install -r requirements.txt

Usage
To run the application, execute:

python main.py
You will be prompted with a menu to login or create a new account. Once logged in, you can manage your passwords through the main menu.

Dependencies
Python 3.x
SQLite
Argon2
EasyGUI
Cryptography
Pyfiglet
Requests
Contributing
Contributions are welcome! Feel free to fork the project and create a pull request with your changes.

License
This project is licensed under the MIT License. See LICENSE for more details.
