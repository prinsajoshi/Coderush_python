'''
Messaging System / Snap chat 

	Functionality: 
Users can create account if they don’t have any 
Users can login using their username and password 
User can search for any other users who are available in the app 
One User can message another user and their messages are stored, don’t  save more then 15 conversations 
Any user can delete msg history on their end 
Database handling using json/txt file handling

'''

import json
import os

class UserAuthentication:
    def __init__(self):
        self.users = {}
        self.load_users()

    def load_users(self):
        # Load users from users.json file
        try:
            with open("users.json", "r") as file:
                self.users = json.load(file)
        except FileNotFoundError:
            self.users = {}

    def save_users(self):
        # Save users to users.json file
        with open("users.json", "w") as file:
            json.dump(self.users, file)

    def login(self):
        # Log in the user
        username = input("\nEnter your username: ")
        password = input("Enter your password: ")

        if username in self.users and self.users[username] == password:
            print("\nLogin successful!")
            self.show_options(username)
        else:
            print("\nInvalid username or password.")

    def create_account(self):
        # Create a new user account
        username = input("Choose a username: ")
        while username in self.users:
            print("\nUsername already exists. Please choose another one.\n")
            username = input("Choose a different username: ")

        password = input("Choose a password: ")
        self.users[username] = password
        self.save_users()
        print("\nAccount created successfully!")

    def show_options(self, username):
        # Show options for the user
        while True:
            print("\nOptions:")
            print("1. Search user and message ")
            print("2. View Messages")
            print("3. Delete message history")
            print("4. Exit")
            
            
            choice = input("\n Enter your choice: ")
            print()

            if choice == '1':
                self.search_user(username)
            elif choice == '2':
                self.view_messages(username)
            elif choice == '3':
                self.delete_messages(username)
            elif choice == '4':
                print("\nExiting the program. Goodbye!")
                break
            else:
                print("\nInvalid choice. Please enter a valid option.")

    def view_messages(self, username):
        # View messages between the user and another user
        recipient_name = input("\nEnter the recipient's name: ")
        with open("messages.json", "r") as file:
            messages = json.load(file)
            count = 0
            for message in messages:
                sender = message['sendername']
                receiver = message['receivername']
                
                if (sender == username and receiver == recipient_name) or (sender == recipient_name and receiver == username):
                    count += 1
                    print(f"{sender}: {message['message']}")
            if count > 15:
                self.delete_oldest_messages(username, recipient_name, count - 15)

    def delete_oldest_messages(self, username, recipient_name, num_to_delete):
        # Delete the oldest messages between two users
        with open("messages.json", "r") as file:
            messages = json.load(file)
        updated_messages = []
        messages_to_delete = num_to_delete
        deleted_count = 0
        for message in messages:
            sender = message['sendername']
            receiver = message['receivername']
            if ((sender == username and receiver == recipient_name) or
                (sender == recipient_name and receiver == username)) and deleted_count < messages_to_delete:
                deleted_count += 1
            else:
                updated_messages.append(message)
        with open("messages.json", "w") as file:
            json.dump(updated_messages, file, indent=4)
        print(f"{deleted_count} oldest message(s) between {username} and {recipient_name} deleted successfully.")

    def search_user(self, username):
        # Search for a user and send a message
        name = input("\nEnter the name you want to search and message: ")
        if name in self.users:
            print(f"{name} is available.")
            message_option = input(f"\nDo you want to message {name}? (yes/no): ")
            if message_option.lower() == "yes":
                message = input("\nEnter your message: ")
                if name in self.users:
                    message_data = {'sendername': username, 'receivername': name, 'message': message}

                    # Check if the messages.json file exists
                    if os.path.exists("messages.json"):
                        # Load existing messages
                        with open("messages.json", "r") as f:
                            existing_messages = json.load(f)
                    else:
                        existing_messages = []

                    # Append new message to the list of messages
                    existing_messages.append(message_data)

                    # Write the updated list of messages to the file
                    with open("messages.json", 'w') as file:
                        json.dump(existing_messages, file, indent=4)  # Indent for readability

                    print("\nMessage sent successfully!")
                else:
                    print(f"{name} is not found in the database.")
        else:
            print(f"{name} is not found in the database.")

    def delete_messages(self, username):
        # Delete message history with a user
        recipient_name = input("\n Enter the recipient's name: ")
        confirmation = input(f"\nDo you want to delete message history with {recipient_name}? (yes/no): ")
        if confirmation.lower() == "yes":
            with open("messages.json", "r") as file:
                messages = json.load(file)
            updated_messages = [message for message in messages if
                                not ((message['sendername'] == username and message['receivername'] == recipient_name) or
                                     (message['sendername'] == recipient_name and message['receivername'] == username))]
            with open("messages.json", "w") as file:
                json.dump(updated_messages, file, indent=4)
            print(f"Message history with {recipient_name} deleted successfully.")
        else:
            print("Message deletion canceled.")

def main():
    auth_system = UserAuthentication()
    print("\n\nWelcome to chithi-email.com")

    while True:
        print("\n1. Login")
        print("2. Create an account")
        print("3. Exit")
        choice = input("\n Enter your choice: ")

        if choice == '1':
            auth_system.login()
        elif choice == '2':
            auth_system.create_account()
        elif choice == '3':
            print("\nExiting the program. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
