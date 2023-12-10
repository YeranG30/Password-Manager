# Password-Manager
Description
The Python-based Password Manager allows users to securely store and manage their passwords, offering features such as password strength assessment, password generation, and easy retrieval of stored passwords. Users can add, fetch, check for password breaches, generate strong passwords, generate passphrases, remove passwords, and change passwords through a user-friendly command-line interface.

# Installation Steps:
Clone into repository 
```
git clone https://github.com/YeranG30/YGs-Password-Manager.git
```
Change Directory 
```
cd Password-Manager
```
Install Dependencies 
```
pip install -r requirements.txt
```
Run Program
```
python3 Pwmngr.py
```

# Section 1: Project Overview
<img width="577" alt="image" src="https://github.com/YeranG30/Password-Manager/assets/74067706/97a18190-0784-48f6-8a52-bcae4484c73d">

The "YG's Password Manager" is a Python-based password management tool designed to enhance security and convenience for users. It leverages Python, SQLite, cryptography, and zxcvbn to offer a comprehensive set of features. Users can create and manage accounts with unique usernames and master passwords, securely store website passwords, and retrieve them as needed. The application checks password strength, alerts users to weak passwords, and even verifies if a password has been compromised in known data breaches. Additionally, it provides password and passphrase generation, password removal, and change capabilities. All data is stored in an encrypted SQLite database, and the tool operates through a command-line interface (CLI) for straightforward usability. "YG's Password Manager" ensures data security, encourages strong passwords, and simplifies the management of sensitive credentials.

# Section 2: Key Features
User Account Management: Users can create accounts with unique usernames and master passwords or log in with existing credentials using the encrypted easygui passwordbox. 

<img width="469" alt="image" src="https://github.com/YeranG30/Password-Manager/assets/74067706/be74cc22-7925-4db4-9dae-8957af992afd">


Secure Password Storage: The application securely stores website names and their corresponding passwords in an SQLite database.

<img width="563" alt="image" src="https://github.com/YeranG30/Password-Manager/assets/74067706/65467d3f-40eb-4063-873e-b0c385d1c04d">

<img width="397" alt="image" src="https://github.com/YeranG30/Password-Manager/assets/74067706/342e0b69-e99d-4cbd-88e5-3cb22e2071ab">


Password Retrieval: Users can retrieve stored passwords for specific websites by providing the website name.

<img width="591" alt="image" src="https://github.com/YeranG30/Password-Manager/assets/74067706/e79d3462-fa80-4a92-8d82-39cd2c6a6c32">

Password Strength Checking: Passwords are evaluated for strength using the zxcvbn library, providing feedback on weak passwords to enhance security. The application enforces password strength requirements to promote strong and secure passwords.

<img width="500" alt="image" src="https://github.com/YeranG30/Password-Manager/assets/74067706/a406e4eb-f447-4a0e-8213-c050cb2bed12">

Password Breach Checking: Users can check if a password has been compromised in known data breaches using the "Have I Been Pwned" API.

<img width="577" alt="image" src="https://github.com/YeranG30/Password-Manager/assets/74067706/73aef1f2-2594-4f5b-9921-e3327a4c9c9f">

<img width="472" alt="image" src="https://github.com/YeranG30/Password-Manager/assets/74067706/a62ea545-eb2d-46be-ab21-6d85185fed0e">


Password and Passphrase Generation: The tool allows users to generate strong, random passwords of specified lengths and passphrases by combining random words from a predefined wordlist.

<img width="418" alt="image" src="https://github.com/YeranG30/Password-Manager/assets/74067706/993d2d52-e326-47c2-af88-a40cb79584c4">

<img width="349" alt="image" src="https://github.com/YeranG30/Password-Manager/assets/74067706/068a174b-aa11-4dea-9b4b-93a34ead6c78">


Password Removal and Change: Users have the capability to remove passwords associated with specific website names or change the password associated with a website.

<img width="532" alt="image" src="https://github.com/YeranG30/Password-Manager/assets/74067706/ccc259f8-af40-4aa5-9dae-79107897659b">


SQLite Database: The application uses an SQLite database to efficiently store user account information and encrypted passwords.

<img width="883" alt="image" src="https://github.com/YeranG30/Password-Manager/assets/74067706/ddb0ecf7-98e7-4352-83e3-1ac53ba2b4b5">

Data Encryption: Passwords stored in the database are encrypted using the Fernet encryption scheme, ensuring that sensitive data remains secure.

<img width="952" alt="image" src="https://github.com/YeranG30/Password-Manager/assets/74067706/e70e98a0-2d0e-434c-8981-e8011a2274a4">

Exiting the Application: Users can safely exit the application, and a scrolling text effect adds a visually engaging element to the experience.


# Section 3: Development Process

Creating the Password Manager:

The Password Manager project began with setting up the Python environment and initializing the project directory. This involved creating a virtual environment to isolate dependencies. I used Git to version-control the project on GitHub, which allowed for easy collaboration and code sharing.

Challenges and Solutions:

One of the main challenges was ensuring the security of user passwords and data. To overcome this, I implemented strong encryption using the Fernet scheme from the cryptography library. This ensured that even if the database was compromised, the stored passwords would remain secure.

Another challenge was implementing password strength checks and password breach checks using the zxcvbn library and the "Have I Been Pwned" API, respectively. This required careful integration and error handling to provide users with useful feedback.

Design Considerations:

Data Encryption: Passwords in the database are encrypted to protect user data. The Fernet encryption scheme was chosen for its robust security features.

Database Management: SQLite was used for database management due to its simplicity and portability. It allows users to store and retrieve their passwords securely.

Password Strength: Passwords are required to meet industry standards for strength, enhancing overall security.


# Section 4: Password Security

The security of user data is a paramount concern in the Password Manager application. To address this, multiple security measures were implemented:

1. Encryption: Encryption is a fundamental security feature in the Password Manager. We used the Fernet encryption scheme from the cryptography library to encrypt and decrypt passwords before storing or retrieving them from the SQLite database. Fernet is a symmetric-key encryption algorithm, meaning it uses the same key for both encryption and decryption. This ensures that only users with the correct key can access their stored passwords. Even if the database is compromised, the encrypted passwords remain unreadable without the encryption key.

2. Password Strength Checks: Enforcing strong password policies is crucial for protecting user accounts. The application uses the zxcvbn library to assess the strength of user-generated passwords. By providing feedback on the strength of passwords, users are encouraged to create robust passwords that are less vulnerable to brute-force attacks. Weak passwords can be easily cracked, putting user accounts at risk. The application's password strength checks help users make informed decisions about their password choices.

3. Password Breach Checks: Passwords are often compromised in data breaches, and users may unknowingly use breached passwords for multiple accounts. To address this issue, the application integrates with the "Have I Been Pwned" API. When users check their passwords, the application hashes the password and sends the first five characters of the hash to the API. If the API returns a matching suffix, it indicates that the password has been breached. This feature helps users identify compromised passwords and take immediate action to change them, enhancing the overall security of their accounts.

   
# Section 5: User Experience


The password manager project is meticulously crafted for a seamless experience on GitHub, where accessibility and collaboration are paramount. With its user-friendly command-line interface (CLI), navigating the codebase and contributing becomes effortless for both developers and users. The GitHub platform serves as the ideal hub for collaborative development, allowing users to access, contribute to, and even fork the project with ease.

The project leverages the power of version control, enabling developers to track changes, manage issues, and merge contributions seamlessly through GitHub's intuitive interface. This collaborative environment fosters transparency and enhances the overall user experience by encouraging community engagement, feedback, and code review. In addition, your project's documentation, including a comprehensive README file, provides clear instructions for installation, usage, and contribution guidelines, ensuring that users and potential collaborators can quickly understand and engage with the project.

# Section 6: What I learned 

My cybersecurity journey has equipped me with essential skills in Python and SQL, enabling me to create secure solutions like my password manager project. Alongside technical expertise, I've developed vital soft skills for effective communication and problem-solving. This project showcases my commitment to data security and user-centric design. I'm well-prepared to contribute to the cybersecurity field.


License
This project is licensed under the MIT License. See LICENSE for more details.
