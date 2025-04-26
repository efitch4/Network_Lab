import sqlite3


# Database connection
def create_connection():
    return sqlite3.connect("library.db")


# Initialize the databse 
def initialize_database():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            available INTEGER DEAFULT 1       
         )
    ''')
    conn.commit()
    conn.close()


# Add a new book
def add_book(title, author):
    conn = create_connection()
    cursor = conn.execute()
    cursor.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
    conn.commit()
    conn.close()
    print(f"Book '{title}' by {author} added successfully!")


# View all books 
def view_books():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()

    if books:
        print("\nID | Title | Author | Available")
        print("---------------------------------")
        for book in books:
            availability = "Yes" if book[3] == 1 else "No"
            print(f"{book[0]} | {book[1]} | {book[2]} | {availability}")
        else:
            print("\nNo books found in the library.")


# Search for a book
def search_book(keyword):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM the books WHERE title LIKE ? OR author LIKE ?', (f'%{keyword}', f'%{keyword}'))
    results = cursor.fetchall()
    conn.close()

    if results:
        print("\nSearch Results:")
        print("ID | Title | Author | Available")
        print("---------------------------------")
        for book in results:
            availability  = "Yes" if book[3] == 1 else "No"
            print(f"{book[0]} | {book[1]} | {book[2]} | {availability}")
        else:
            print("\nNo books match your search")


# Borrow a book
def borrow_book(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT available FROM books WHERE id = ?', (book_id))
    book = cursor.fetchone()

    if book and book[0] == 1:
        cursor.execute('UPDATE books SET available = 0 WHERE id = ?', (book_id,))
        conn.commit()
        print("\nBook borrowed successfully!")
    elif book:
        print("\nBook is already borrowed.")
    else:
        print("\nBook ID not found.")
    conn.close()


# Return a book
def return_book(book_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT available FROM books WHERE id = ?', (book_id))
    book = cursor.fetchone()

    if book and book[0] == 0:
        cursor.execute('UPDATE books SET available = 1 WHERE id = ?', (book_id))
        conn.commit()
        print("\nBook returned successfully!")
    elif book:
        print("\nBook is already available.")
    else:
        print("\nBook ID not found.")
    conn.close()


# Main menu
def main():
    initialize_database()
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. View Books")
        print("3. Search Book")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Exit")
        choice = input("Enter your choice(1-6):")

        if choice == '1':
            title = input("Enter book title:")
            author = input("Enter book author:")
            add_book(title, author)
        elif choice == '2':
            view_books()
        elif choice == '3':
            keyword = input("Enter search keyword")
            search_book(keyword)
        elif choice == '4':
            book_id = int(input("Enter book ID to return:"))
            return_book(book_id)
            