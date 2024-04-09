'''
Movie Ticketing System

Functionality:

Users can sign up without any account.
Each user has a unique username, and the system ensures uniqueness.
User history of all previous movies watched is recorded.
After logging in, users can book tickets for available movies.
Users can select seats based on availability.
Once a seat is booked, it becomes unavailable for other users.
Database handling using json/txt file handling 


'''

import json
from json.decoder import JSONDecodeError
from movie import MovieTicketingSystem

class LoginSystem:
    def __init__(self):
        # Load existing user data from JSON file or initialize an empty dictionary
        try:
            with open("users.json", "r") as file:
                # Try to load user data from JSON file
                self.users_data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            # If the file is not found or empty, initialize an empty dictionary
            self.users_data = {}

    def check_username(self, username):
        # Check if the username is already taken
        if username in self.users_data:
            print("Username is taken. Please choose another username.")
            return False
        else:
            return True

    def create_account(self, username, password):
        # Add new user to the user data dictionary
        self.users_data[username] = {"password": password}
        # Save updated user data to JSON file
        with open("users.json", "w") as file:
            json.dump(self.users_data, file)
        print("Account created successfully!")

    def login(self):
        # Prompt the user to enter a username and password
        print("Welcome to the Movie Ticketing System!")
        print("Please enter your username and password to continue.")
        
        while True:
            username = input("Username: ")
            password = input("Password: ")

            # Check if the username exists and password matches
            if username in self.users_data and self.users_data[username]["password"] == password:
                print("Login successful!")
                return True
            elif self.check_username(username):
                # If username not found, create a new account
                self.create_account(username, password)
                return True
            else:
                print("Invalid username or password. Please try again.")

def main():
    login_system = LoginSystem()
    if login_system.login():
        mts = MovieTicketingSystem()
        mts.main_menu()

if __name__ == "__main__":
    main()
