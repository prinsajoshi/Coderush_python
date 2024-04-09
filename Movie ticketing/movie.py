import json

class MovieTicketingSystem:
    def __init__(self):
        # Initialize an empty list to store movies watched by users
        self.movies_watched = []

    def display_home_page(self):
        # Display the home page menu options
        print("Welcome to the Movie Ticketing System!\n1. History of My Movies\n2. Book Tickets\n3. Exit\n")

    def display_movie_history(self, username):
        # Display the booking history for a user
        with open("users.json", "r") as file:
            users_data = json.load(file)

        if username not in users_data:
            print("\nNo booking history found for this user.\n")
            return

        booking_history = users_data[username]
        print("Booking History:\n")

        for key, value in booking_history.items():
            if key != "password":
                print(f"{key}: {value}")

    def book_tickets(self, username):
        # Book tickets for a selected movie
        print("\nBook Tickets:\nSelect a movie to book tickets for:\n1. Batman\n2. Spiderman\n3. Antman\n4. Ironman\n5. Superman\n6. Back to Main Menu\n")
        movie_choice = input("Enter the movie number (1-6): ")

        if movie_choice == '6':
            return

        try:
            movie_choice = int(movie_choice)
        except ValueError:
            print("\nInvalid choice. Please enter a number between 1 and 6.\n")
            return

        if movie_choice < 1 or movie_choice > 5:
            print("\nInvalid choice. Please enter a number between 1 and 5.\n")
            return

        # Mapping movie names to corresponding classes
        movie_classes = {
            1: "Batman",
            2: "Spiderman",
            3: "Antman",
            4: "Ironman",
            5: "Superman"
        }

        selected_movie = movie_classes.get(movie_choice)
        if selected_movie:
            print(f"Seating arrangement for {selected_movie}:")
            self.display_seating_arrangement(selected_movie)
            row = int(input("Enter the row number (1-9): "))
            column = int(input("Enter the column number (1-9): "))

            if self.book_seat(selected_movie, row, column, username):
                print("\nTicket booked successfully!\n")
        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.\n")

    def display_seating_arrangement(self, movie):
        # Display the seating arrangement for a movie
        with open("movies.json", "r") as file:
            data = json.load(file)
            seats = data[movie]["seats"]

        print("  " + " ".join([str(i) for i in range(1, 10)]))
        for i in range(9):
            print(i + 1, end=" ")
            for j in range(9):
                print(seats[i][j], end=" ")
            print()

    def book_seat(self, movie, row, column, username):
        # Book a seat for a movie
        with open("movies.json", "r") as file:
            data = json.load(file)
            seats = data[movie]["seats"]

        if row < 1 or row > 9 or column < 1 or column > 9:
            print("Invalid seat selection. Please enter valid row and column numbers.")
            return False

        if seats[row - 1][column - 1] == 'B':
            print("Seat already booked. Please select another seat.")
            return False

        seats[row - 1][column - 1] = 'B'
        self.save_seating_arrangement(data)

        # Update user booking data
        with open("users.json", "r+") as file:
            users_data = json.load(file)
            if username in users_data:
                if movie in users_data[username]:
                    users_data[username][movie].append((row, column))
                else:
                    users_data[username][movie] = [(row, column)]
            else:
                users_data[username] = {movie: [(row, column)]}
            file.seek(0)
            json.dump(users_data, file)
            file.truncate()

        return True

    def save_seating_arrangement(self, data):
        # Save the updated seating arrangement to file
        with open("movies.json", "w") as file:
            json.dump(data, file)
            print("Seating arrangement updated successfully.")

    def main_menu(self):
        # Display the main menu and handle user input
        while True:
            self.display_home_page()
            choice = input("Enter your choice (1-3): ")
            if choice == '1':
                username = input("Enter your username: ")
                self.display_movie_history(username)
            elif choice == '2':
                username = input("Enter your username: ")
                self.book_tickets(username)
            elif choice == '3':
                print("Exiting Movie Ticketing System. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

def main():
    # Create an instance of the MovieTicketingSystem and start the main menu
    mts = MovieTicketingSystem()
    mts.main_menu()

if __name__ == "__main__":
    main()
