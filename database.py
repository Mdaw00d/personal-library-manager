import sqlite3

class Database:
    def __init__(self, db_name="library.db"):
        """Initialize the SQLite database and create the books table if it doesn't exist."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create the books table if it does not exist."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            genre TEXT,
            read INTEGER DEFAULT 0
        )
        """)
        self.conn.commit()

    def add_book(self, title, author, year, genre, read):
        """Insert a new book into the database."""
        self.cursor.execute(
            "INSERT INTO books (title, author, year, genre, read) VALUES (?, ?, ?, ?, ?)",
            (title, author, year, genre, read),
        )
        self.conn.commit()

    def delete_book(self, title):
        """Remove a book from the database by title."""
        self.cursor.execute("DELETE FROM books WHERE title = ?", (title,))
        self.conn.commit()

    def find_books(self, search_text):
        """Find books by title or author."""
        self.cursor.execute(
            "SELECT * FROM books WHERE LOWER(title) LIKE ? OR LOWER(author) LIKE ?",
            (f"%{search_text}%", f"%{search_text}%"),
        )
        return self.cursor.fetchall()

    def update_book(self, book_id, title, author, year, genre, read):
        """Update book details."""
        self.cursor.execute(
            "UPDATE books SET title=?, author=?, year=?, genre=?, read=? WHERE id=?",
            (title, author, year, genre, read, book_id),
        )
        self.conn.commit()

    def get_all_books(self):
        """Retrieve all books from the database."""
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

    def get_reading_progress(self):
        """Calculate reading progress."""
        self.cursor.execute("SELECT COUNT(*) FROM books")
        total_books = self.cursor.fetchone()[0]

        self.cursor.execute("SELECT COUNT(*) FROM books WHERE read = 1")
        completed_books = self.cursor.fetchone()[0]

        completion_rate = (completed_books / total_books * 100) if total_books > 0 else 0
        return total_books, completion_rate

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
