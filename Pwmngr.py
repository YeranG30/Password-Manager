# Import required modules and packages for the application.
from cryptography.fernet import Fernet
from zxcvbn import zxcvbn
from easygui import passwordbox
import random
import string
import time
import hashlib
import requests
import pyfiglet
import sqlite3
from passlib.hash import argon2
from passgen import passgen

# Main class for managing passwords.
class PasswordManager:
    # Initialize the application, set up encryption keys, and call login.
    def __init__(self):
        # Encryption key for Fernet
        self.key = b'CxVuqDntmYR7WKpDfUsEtYXw5b2rJBuTpuBlfSqKe4w='
        self.cipher_suite = Fernet(self.key)
        # Initialize database and ensure necessary columns exist
        self.init_db()
        self.ensure_password_column_exists()
        # Start the login process
        self.login()
        # Run the main application loop
        self.run()
        # Variable to store the current user's ID
        self.current_user_id = None

    # Display a banner at the start of the application
    def banner(self):
        cool_banner = pyfiglet.figlet_format("YG's Password Manager", font="slant", justify="center")
        print(cool_banner)

    # Set up the SQLite database framework
    def init_db(self):
        # Connect to SQLite database
        self.conn = sqlite3.connect("newpasswords.db")
        self.cursor = self.conn.cursor()
        # Create users table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            );
        """)
        # Create passwords table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT,
                password TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        self.conn.commit()

    # Ensure the password column exists in the users table
    def ensure_password_column_exists(self):
        # Fetch existing columns in the users table
        self.cursor.execute("PRAGMA table_info(users);")
        columns = [column[1] for column in self.cursor.fetchall()]
        # Add 'password' column if it doesn't exist
        if 'password' not in columns:
            self.cursor.execute("ALTER TABLE users ADD COLUMN password TEXT")
            self.conn.commit()

    # Manage user login and account creation
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
                # Handle user login
                username = input("Enter your username: ")
                password = input("Enter your password: ")
                # Fetch user ID and password from the database
                self.cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
                row = self.cursor.fetchone()

                if row:
                    user_id, stored_hashed_password = row
                    # Verify the entered password
                    if argon2.verify(password, stored_hashed_password):
                        self.current_user_id = user_id  # Store the user's ID
                        print("\nLogin successful!\n")
                        return True
                    else:
                        print("\nIncorrect credentials.\n")
                else:
                    print("\nIncorrect credentials.\n")

            elif choice == '2':
                # Handle new account creation
                username = input("Enter your new username: ")
                password = input("Enter your new master password: ")
                hashed_password = argon2.hash(password)
                try:
                    self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                                        (username, hashed_password))
                    self.conn.commit()
                    print("\nAccount successfully created! Please login with your new credentials.\n")
                except sqlite3.IntegrityError:
                    print("\nUsername already exists. Choose a different username.\n")

            elif choice == '3':
                # Exit the application
                print("Exiting...")
                exit(0)

            else:
                print("\nInvalid choice.\n")

    # Main application menu
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

            # Handle different options based on user choice
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

    # Check the strength of a password using zxcvbn library
    def is_password_strong(self, password):
        results = zxcvbn(password)
        # 'score' is a rating from 0 (worst) to 4 (best)
        if results['score'] < 3:
            print(f"Password strength is weak: {results['feedback']['warning']}")
            for suggestion in results['feedback']['suggestions']:
                print(suggestion)
            return False
        return True

    # Add a password to the database
    def add_password(self):
        pw_name = input("Enter the website used for the password: ")
        password = passwordbox("Enter the password: ")

        # Check password strength
        if not self.is_password_strong(password):
            choice = input("Do you want to continue adding the password? (Yes/No): \n")
            if choice.lower() not in {"y", "yes", "ye"}:
                print("Password addition cancelled.")
                return

        # Check if the password for this website already exists for this user
        self.cursor.execute("SELECT password FROM passwords WHERE name=? AND user_id=?",
                            (pw_name, self.current_user_id))
        row = self.cursor.fetchone()
        if row:
            print(f"A password with the name '{pw_name}' already exists.")
            return

        # Insert the new password record associated with the current user
        encrypted_password = self.cipher_suite.encrypt(password.encode())
        self.cursor.execute("INSERT INTO passwords (user_id, name, password) VALUES (?, ?, ?)",
                            (self.current_user_id, pw_name, encrypted_password))
        self.conn.commit()
        print("Password added successfully.")

    # Fetch a password from the database
    def fetch_password(self):
        pw_name = input("Enter the website of the password you would like to fetch, case sensitively: ")
        self.cursor.execute("SELECT password FROM passwords WHERE name=? AND user_id=?",
                            (pw_name, self.current_user_id))
        row = self.cursor.fetchone()
        if row:
            encrypted_password = row[0]
            decrypted_password = self.cipher_suite.decrypt(encrypted_password).decode()
            print(f"Password for {pw_name}: {decrypted_password}")
        else:
            print(f"Password for {pw_name} not found.")

    # Check if a password is in 'pwnedpasswords' wordlists
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

    # Generate a strong password
    def generate_strong_password(self):
        password = passgen(length=16)
        print(f"Generated strong password: {password}")

    # Generate a passphrase
    def generate_passphrase(self):
        wordlist = [
            # List of words for passphrase generation
            "apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew",
            # ... (rest of the wordlist)
        ]

        passphrase = ' '.join(random.choice(wordlist) for _ in range(4))
        print(f"Generated passphrase: {passphrase}")

    # Exit the application
    def exit_app(self):
        exit_message = "Exiting Yeran's Password Manager. . . "
        self.scrolling_text_effect(exit_message)
        print("Exit Successful")

    # Cool text effect for exit message
    def scrolling_text_effect(self, text, repeat=3):
        scroll_speed = .02  # Adjust the scroll speed here
        text_length = len(text)

        for _ in range(repeat):
            for i in range(text_length + 1):
                formatted_text = "".join(char.upper() if idx >= i else char for idx, char in enumerate(text))
                print(formatted_text, end="\r")
                time.sleep(scroll_speed)

            print(" " * text_length, end="\r")

    # User can edit password
    def change_password(self):
        pw_name = input("Enter the name of the password you want to configure: ")

        # Fetch encrypted password from database
        self.cursor.execute("SELECT password FROM passwords WHERE name=?", (pw_name,))
        row = self.cursor.fetchone()
        if row:
            encrypted_password = row[0]

            # Get a new password and update it in the database
            new_password = passwordbox("Enter the new password: ")
            while not self.is_password_strong(new_password):
                print("Password does not meet industry standards for strength!")
                choice = input("Do you want to continue configuring the password? (Yes/No): \n")
                if choice.lower() not in {"y", "yes", "ye"}:
                    print("Password configuration cancelled.")
                    return
                new_password = passwordbox("Enter the new password: ")

            self.cursor.execute("UPDATE passwords SET password=? WHERE name=?",
                                (self.cipher_suite.encrypt(new_password.encode()), pw_name))
            self.conn.commit()
            print("Password configured successfully.")
        else:
            print(f"Password for {pw_name} not found.")

    # Remove a password
    def remove_password(self):
        pw_name = input("Enter the name of the website that you want the password removed: ")

        # Check if the password exists and remove it
        self.cursor.execute("SELECT password FROM passwords WHERE name=?", (pw_name,))
        row = self.cursor.fetchone()

        if row:
            self.cursor.execute("DELETE FROM passwords WHERE name=?", (pw_name,))
            self.conn.commit()
            print(f"Password for {pw_name} has been removed.")
        else:
            print(f"Password for {pw_name} not found.")

    # Clear the console (placeholder function)
    def clear_console(self):
        pass

# Run the password manager
if __name__ == "__main__":
    password_manager = PasswordManager()
    while True:
        if password_manager.login():
            password_manager.run()
            break
