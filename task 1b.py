from cryptography.fernet import Fernet
import json
import os

class PasswordManager:
    def __init__(self, key_file="key.key", data_file="passwords.json"):
        self.key_file = key_file
        self.data_file = data_file
        self.key = self.load_or_create_key()
        self.cipher_suite = Fernet(self.key)
        self.passwords = self.load_passwords()

    def load_or_create_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as key_file:
                key = key_file.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(key)
        return key

    def load_passwords(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "rb") as data_file:
                encrypted_data = data_file.read()
                decrypted_data = self.cipher_suite.decrypt(encrypted_data)
                passwords = json.loads(decrypted_data)
        else:
            passwords = {}
        return passwords

    def save_passwords(self):
        encrypted_data = self.cipher_suite.encrypt(json.dumps(self.passwords).encode())
        with open(self.data_file, "wb") as data_file:
            data_file.write(encrypted_data)

    def add_password(self, website, username, password):
        if website in self.passwords:
            print(f"Password for {website} already exists. Updating...")
        self.passwords[website] = {"username": username, "password": password}
        self.save_passwords()
        print(f"Password for {website} added successfully.")

    def get_password(self, website):
        if website in self.passwords:
            return self.passwords[website]
        else:
            return None

    def list_websites(self):
        return list(self.passwords.keys())


if __name__ == "__main__":
    manager = PasswordManager()

    while True:
        print("\nPassword Manager Menu:")
        print("1. Add a password")
        print("2. Get a password")
        print("3. List websites")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            website = input("Enter the website: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            manager.add_password(website, username, password)

        elif choice == "2":
            website = input("Enter the website: ")
            result = manager.get_password(website)
            if result:
                print(f"Username: {result['username']}")
                print(f"Password: {result['password']}")
            else:
                print(f"Password for {website} not found.")

        elif choice == "3":
            websites = manager.list_websites()
            if websites:
                print("List of websites:")
                for website in websites:
                    print(website)
            else:
                print("No passwords stored.")

        elif choice == "4":
            print("Exiting Password Manager.")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
