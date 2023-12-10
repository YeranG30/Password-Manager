# Password-Manager
Description
The Python-based Password Manager allows users to securely store and manage their passwords, offering features such as password strength assessment, password generation, and easy retrieval of stored passwords. Users can add, fetch, check for password breaches, generate strong passwords, generate passphrases, remove passwords, and change passwords through a user-friendly command-line interface.

Features
User Login and Account Creation
Secure Password Storage
Password Retrieval
Password Strength Check
Password Breach Check
Password Generation
Passphrase Generation
Password Removal
Password Change
SQLite Database
Command-Line Interface (CLI)
Data Encryption
Password Strength Requirements
Safe Application Exit


# Clone the repository:
```
git clone https://github.com/YeranG30/YGs-Password-Manager.git
```

# Navigate into the project directory:
```
cd Password-Manager
```

# Install the required packages:
```
pip install -r requirements.txt
```

# To run the application, execute:
```
python3 Pwmngr.py
```
# Section 1: Project Overview
<img width="529" alt="image" src="https://github.com/YeranG30/Password-Manager/assets/74067706/13e91d6d-cedf-4c32-a3e8-6ff9e26e2015">

The "YG's Password Manager" is a Python-based password management tool designed to enhance security and convenience for users. It leverages Python, SQLite, cryptography, and zxcvbn to offer a comprehensive set of features. Users can create and manage accounts with unique usernames and master passwords, securely store website passwords, and retrieve them as needed. The application checks password strength, alerts users to weak passwords, and even verifies if a password has been compromised in known data breaches. Additionally, it provides password and passphrase generation, password removal, and change capabilities. All data is stored in an encrypted SQLite database, and the tool operates through a command-line interface (CLI) for straightforward usability. "YG's Password Manager" ensures data security, encourages strong passwords, and simplifies the management of sensitive credentials.

# Section 2: Key Features
<img width="469" alt="image" src="https://github.com/YeranG30/Password-Manager/assets/74067706/be74cc22-7925-4db4-9dae-8957af992afd">
User Account Management: Users can create accounts with unique usernames and master passwords or log in with existing credentials.

Secure Password Storage: The application securely stores website names and their corresponding passwords in an SQLite database.

Password Retrieval: Users can retrieve stored passwords for specific websites by providing the website name.

Password Strength Checking: Passwords are evaluated for strength using the zxcvbn library, providing feedback on weak passwords to enhance security.

Password Breach Checking: Users can check if a password has been compromised in known data breaches using the "Have I Been Pwned" API.

Password and Passphrase Generation: The tool allows users to generate strong, random passwords of specified lengths and passphrases by combining random words from a predefined wordlist.

Password Removal and Change: Users have the capability to remove passwords associated with specific website names or change the password associated with a website.

SQLite Database: The application uses an SQLite database to efficiently store user account information and encrypted passwords.

Command-Line Interface (CLI): The application operates through a text-based command-line interface, providing users with a straightforward and efficient way to manage their passwords.

Data Encryption: Passwords stored in the database are encrypted using the Fernet encryption scheme, ensuring that sensitive data remains secure.

Password Strength Requirements: The application enforces password strength requirements to promote strong and secure passwords.

Exiting the Application: Users can safely exit the application, and a scrolling text effect adds a visually engaging element to the experience.

# Section 3: Development Process

Describe the steps you took to create the password manager.
Discuss the challenges you faced and how you overcame them.
Mention any design considerations you made, such as data encryption and database management.

# Section 4: Code Highlights

Share specific code snippets that demonstrate your coding skills.
Explain how certain functionalities are implemented in your code.
Include comments to make the code more understandable.

# Section 5: Password Security

Dive deeper into the security aspects of your application.
Explain how you used encryption to protect user data.
Discuss the importance of password strength checks and breach checks.

# Section 6: User Experience

Highlight how your password manager is user-friendly.
Describe the user interface (command-line interface in this case).
Mention any user-centric design choices you made.


License
This project is licensed under the MIT License. See LICENSE for more details.
