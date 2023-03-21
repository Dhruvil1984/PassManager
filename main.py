import sqlite3
import random
import string

class PasswordManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS passwords(
                id INTEGER PRIMARY KEY,
                account TEXT,
                password TEXT
            )
        """)
        self.conn.commit()

    def generate_password(self, length=10):
        """Generate a random password with the given length."""
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))

    def store_password(self, account, password):
        """Store the given password for the given account."""
        self.cur.execute("INSERT INTO passwords(account, password) VALUES (?, ?)", (account, password))
        self.conn.commit()

    def retrieve_password(self, account):
        """Retrieve the password for the given account."""
        self.cur.execute("SELECT password FROM passwords WHERE account=?", (account,))
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return None

    def write_to_file(self, file_name):
        """Write the stored passwords to a text file, line-by-line."""
        with open(file_name, 'w') as f:
            self.cur.execute("SELECT account, password FROM passwords")
            results = self.cur.fetchall()
            for result in results:
                f.write(f"{result[0]} {result[1]}\n")

    def close(self):
        """Close the database connection."""
        self.conn.close()

if __name__ == '__main__':
    password_manager = PasswordManager('passwords.db')

    # Generate a password and store it for an account
    account = input("Enter account name: ")
    password = password_manager.generate_password()
    password_manager.store_password(account, password)
    print(f"Password for {account} is {password}")

    # Retrieve a password for an account
    account = input("Enter account name: ")
    password = password_manager.retrieve_password(account)
    if password:
        print(f"Password for {account} is {password}")
    else:
        print(f"No password found for {account}")

    # Write stored passwords to a text file
    file_name = input("Enter file name to write stored passwords: ")
    password_manager.write_to_file(file_name)

    password_manager.close()
