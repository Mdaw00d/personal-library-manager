from database import Database

class BookCollection:
    """A class to manage a collection of books using SQLite database storage."""
    
    def __init__(self):
        self.db = Database()

    def create_new_book(self):
        """Add a new book."""
        book_title = input("Enter book title: ")
        book_author = input("Enter author: ")
        publication_year = input("Enter publication year: ")
        book_genre = input("Enter genre: ")
        is_book_read = input("Have you read this book? (yes/no): ").strip().lower() == "yes"

        self.db.add_book(book_title, book_author, publication_year, book_genre, int(is_book_read))
        print("Book added successfully!\n")

    def delete_book(self):
        """Remove a book."""
        book_title = input("Enter the title of the book to remove: ")
        self.db.delete_book(book_title)
        print("Book removed successfully!\n")

    def find_book(self):
        """Search for books."""
        search_text = input("Enter search term (title or author): ").lower()
        books = self.db.find_books(search_text)

        if books:
            print("Matching Books:")
            for index, book in enumerate(books, 1):
                reading_status = "Read" if book[5] else "Unread"
                print(f"{index}. {book[1]} by {book[2]} ({book[3]}) - {book[4]} - {reading_status}")
        else:
            print("No matching books found.\n")

    def update_book(self):
        """Modify book details."""
        book_title = input("Enter the title of the book you want to edit: ")
        books = self.db.find_books(book_title)

        if books:
            book_id = books[0][0]
            new_title = input(f"New title ({books[0][1]}): ") or books[0][1]
            new_author = input(f"New author ({books[0][2]}): ") or books[0][2]
            new_year = input(f"New year ({books[0][3]}): ") or books[0][3]
            new_genre = input(f"New genre ({books[0][4]}): ") or books[0][4]
            new_read = input("Have you read this book? (yes/no): ").strip().lower() == "yes"

            self.db.update_book(book_id, new_title, new_author, new_year, new_genre, int(new_read))
            print("Book updated successfully!\n")
        else:
            print("Book not found!\n")

    def show_all_books(self):
        """Display all books."""
        books = self.db.get_all_books()

        if not books:
            print("Your collection is empty.\n")
            return

        print("Your Book Collection:")
        for index, book in enumerate(books, 1):
            reading_status = "Read" if book[5] else "Unread"
            print(f"{index}. {book[1]} by {book[2]} ({book[3]}) - {book[4]} - {reading_status}")
        print()

    def show_reading_progress(self):
        """Calculate reading progress."""
        total_books, completion_rate = self.db.get_reading_progress()
        print(f"Total books in collection: {total_books}")
        print(f"Reading progress: {completion_rate:.2f}%\n")

    def start_application(self):
        """Run the main application loop."""
        while True:
            print("\n📚 Welcome to Your Book Collection Manager! 📚")
            print("1. Add a new book")
            print("2. Remove a book")
            print("3. Search for books")
            print("4. Update book details")
            print("5. View all books")
            print("6. View reading progress")
            print("7. Exit")
            user_choice = input("Please choose an option (1-7): ")

            if user_choice == "1":
                self.create_new_book()
            elif user_choice == "2":
                self.delete_book()
            elif user_choice == "3":
                self.find_book()
            elif user_choice == "4":
                self.update_book()
            elif user_choice == "5":
                self.show_all_books()
            elif user_choice == "6":
                self.show_reading_progress()
            elif user_choice == "7":
                self.db.close_connection()
                print("Thank you for using Book Collection Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    book_manager = BookCollection()
    book_manager.start_application()
