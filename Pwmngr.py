#Import required modules and packages for the application.
from cryptography.fernet import Fernet
from easygui import passwordbox
import random
import string
import time
import hashlib
import requests
import pyfiglet
import sqlite3
import os
from passlib.hash import argon2



#Main class for managing passwords.
class PasswordManager:
    # Initialize the application, set up encryption keys, and call login.
    def __init__(self):
        self.key = b'CxVuqDntmYR7WKpDfUsEtYXw5b2rJBuTpuBlfSqKe4w='
        self.cipher_suite = Fernet(self.key)
        self.init_db()
        self.login()
        self.run()

# shows the jaw-dropping banner
    def banner(self):
        cool_banner = pyfiglet.figlet_format("YG's Password Manager", font="slant", justify="center")
        print(cool_banner)

#sets up sql framework
    def init_db(self):
        self.conn = sqlite3.connect("passwords.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                password TEXT
            );
        """)
        self.conn.commit()

#manages user login and account creation
    def login(self):
        self.banner()
        while True:
            print("\n" + "=" * 50)
            print(" " * 15 + "WELCOME TO YG's PASSWORD MANAGER")
            print("=" * 50 + "\n")

            print("1. Login")
            print("2. Create an account")
            print("3. Exit\n")

            choice = input("Enter choice: ")

            if choice == '1':
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                hashed_password = argon2.hash(password)

                self.cursor.execute("SELECT password_hash FROM users WHERE username=?", (username,))
                row = self.cursor.fetchone()

                if row:
                    stored_hashed_password = row[0]
                    if argon2.verify(password, stored_hashed_password):
                        print("\nLogin successful!\n")
                        return True
                    else:
                        print("\nIncorrect password.\n")
                else:
                    print("\nUsername does not exist.\n")


            elif choice == '2':
                username = input("Enter your new username: ")  # This should work
                password = input("Enter your new master password: ")  # Temporary, for debugging
                hashed_password = argon2.hash(password)
                try:
                    self.cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
                                        (username, hashed_password))
                    self.conn.commit()
                    print("\nAccount successfully created! Please login with your new credentials.\n")
                    continue
                except sqlite3.IntegrityError:
                    print("\nUsername already exists. Choose a different username.\n")
                    continue  # Go back to the login screen
            elif choice == '3':
                print("Exiting...")
                exit(0)
            elif choice == '3':
                print("Exiting...")
                exit(0)
            else:
                print("\nInvalid choice.\n")
            if row:
                stored_hashed_password = row[0]
                if stored_hashed_password == hashed_password:
                    self.clear_console()  # <-- Clear console after successful login
                    print("\nLogin successful!\n")
                    return True
    #main menu
    def run(self):
        self.banner()
        while True:
            print("\nMain Menu:\n-------------------------------------------------------------------------")
            print("1. Add Password")
            print("2. Fetch Password")
            print("3. Check for Password Breach")
            print("4. Generate Strong Password")
            print("5. Generate Passphrase")
            print("6. Remove Password")
            print("7. Change Password")
            print("8. Exit")
            option = input("\nEnter Choice: ")

            if option == '1':
                self.add_password()
            elif option == '2':
                self.fetch_password()
            elif option == '3':
                self.check_password_wordlist()
            elif option == "4":
                self.generate_strong_password()
            elif option == "5":
                self.generate_passphrase()
            elif option == '6':
                self.remove_password()
            elif option == '7':
                self.change_password()
            elif option == '8':
                self.exit_app()
                break
            else:
                print("Invalid Choice, Please choose again! ")

    # checks password strength (need to make this more selective)
    def check_password_strength(self, password):
        length_req_met = len(password) >= 12
        uppercase_req_met = any(c.isupper() for c in password)
        lowercase_req_met = any(c.islower() for c in password)
        digit_req_met = any(c.isdigit() for c in password)
        special_char_req_met = any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for c in password)

        if all([length_req_met, uppercase_req_met, lowercase_req_met, digit_req_met, special_char_req_met]):
            return True
        else:
            return False

#Adds a password to the database.
    def add_password(self):
        pw_name = input("Enter the website used for the password: ")
        password = passwordbox("Enter the password: ")
        # Check password strength
        if not self.check_password_strength(password):
            print("Password does not meet industry standards for strength.")
            choice = input("Do you want to continue adding the password? (Yes/No): \n")
            if choice.lower() not in {"y", "yes", "ye"}:
                print("Password addition cancelled.")
                return
        self.cursor.execute("SELECT password FROM passwords WHERE name=?", (pw_name,))
        row = self.cursor.fetchone()
        if row:
            print(f"A password with the name '{pw_name}' already exists.")
            return
        self.cursor.execute("INSERT INTO passwords (name, password) VALUES (?, ?)",
                            (pw_name, self.cipher_suite.encrypt(password.encode())))
        self.conn.commit()
        print("Password added successfully.")

# fetches password from db
    def fetch_password(self):
        pw_name = input("Enter the website of the password you would like to fetch, case sensitively: ")
        self.cursor.execute("SELECT password FROM passwords WHERE name=?", (pw_name,))
        row = self.cursor.fetchone()
        if row:
            encrypted_password = row[0]
            decrypted_password = self.cipher_suite.decrypt(encrypted_password).decode()
            print(f"Password for {pw_name}: {decrypted_password}")
        else:
            print(f"Password for {pw_name} not found.")

#checks to see if pw is in 'pwnedpasswords' wordlists (vuln to bruteforcing if found within wordlist)
    def check_password_wordlist(self):
        password = passwordbox("Enter the password to check for breaches: ")
        sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
        prefix, suffix = sha1_hash[:5], sha1_hash[5:]
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        for line in response.text.splitlines():
            hash_prefix, count = line.split(":")
            if hash_prefix == suffix:
                print("❗❗⚠️⚠️Password has been breached, please change it!⚠️⚠️❗❗")
                return
        print("Password is not compromised.✅😅")

# generates strong password ( not realistic password, need to make more personal)
    def generate_strong_password(self):
        length = 16
        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase
        digits = string.digits
        special_characters = string.punctuation
        pool = lowercase_letters + uppercase_letters + digits + special_characters
        password = random.choice(lowercase_letters) + random.choice(uppercase_letters) + random.choice(digits) + random.choice(special_characters)
        password += "" .join(random.choice(pool) for _ in range(length - 4))
        print(f"Generated strong password:{password}")

# gerneartes passphrase ( need to import some more to make it diverse)
    def generate_passphrase(self):
        wordlist = ["apple", "banana", "cherry", "dog", "elephant", "frog"]
        passphrase = ' '.join(random.choice(wordlist) for _ in range(4))
        print(f"Generated passphrase: {passphrase}")

# exits app
    def exit_app(self):
        exit_message = "Exiting Yeran's Password Manager. . . "
        self.scrolling_text_effect(exit_message)
        print("Exit Successful")
# cool text effect

    def scrolling_text_effect(self, text, repeat=3):
        scroll_speed = .02  # Adjust the scroll speed here
        text_length = len(text)

        for _ in range(repeat):
            for i in range(text_length + 1):
                formatted_text = "".join(char.upper() if idx >= i else char for idx, char in enumerate(text))
                print(formatted_text, end="\r")
                time.sleep(scroll_speed)

            print(" " * text_length, end="\r")

# user can edit password
    def change_password(self):
        pw_name = input("Enter the name of the password you want to configure: ")

        # Fetch encrypted password from database instead of in-memory dictionary
        self.cursor.execute("SELECT password FROM passwords WHERE name=?", (pw_name,))
        row = self.cursor.fetchone()
        if row:
            encrypted_password = row[0]

            # Rest of your code for getting a new password
            new_password = passwordbox("Enter the new password: ")
            while not self.check_password_strength(new_password):
                print("Password does not meet industry standards for strength!")
                choice = input("Do you want to continue configuring the password? (Yes/No): \n")
                if choice.lower() not in {"y", "yes", "ye"}:
                    print("Password configuration cancelled.")
                    return
                new_password = passwordbox("Enter the new password: ")

            # Update the password in the database
            self.cursor.execute("UPDATE passwords SET password=? WHERE name=?",
                                (self.cipher_suite.encrypt(new_password.encode()), pw_name))
            self.conn.commit()
            print("Password configured successfully.")
        else:
            print(f"Password for {pw_name} not found.")
# removes password
    def remove_password(self):
        pw_name = input("Enter the name of the website that you want the password removed: ")

        # First check if the password entry for the given name exists
        self.cursor.execute("SELECT password FROM passwords WHERE name=?", (pw_name,))
        row = self.cursor.fetchone()

        if row:
            # Perform the deletion from the database
            self.cursor.execute("DELETE FROM passwords WHERE name=?", (pw_name,))
            self.conn.commit()
            print(f"Password for {pw_name} has been removed.")
        else:
            print(f"Password for {pw_name} not found.")


if __name__ == "__main__":
    password_manager = PasswordManager()
    while True:
        if password_manager.login():
            password_manager.run()
            break