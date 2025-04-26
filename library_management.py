# Advanced Library Management System

class Library:
    def __init__(self, filename="library.txt"):
        self.filename = filename
        self.books = {}
        self.load_books()

    def load_books(self):
        """Load books from the text file into the system."""
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    title, author, available = line.strip().split('|')
                    self.books[title] = {'author': author, 'available': available == 'True'}
        except FileNotFoundError:
            print(f"File '{self.filename}' not found. Starting with an empty library")

    def save_books(self):
        """Save the current library to the text file."""
        with open(self.filename, 'w') as file:
            for title, details in self.books.items():
                file.write(f"{title}|{details['author']}|{details['available']}\n")

    def add_book(self, title, author):
        """ Add a new book to the library."""
        if title in self.books:
            print(f"Book '{title}' already exists.")
            return
        self.books[title] = {'author': author, 'available': True}
        self.save_books()
        print(f"Book {'title'} by {author} added.")

    def remove_book(self, title):
        """ Remove a book from the library."""
        if title in self.books:
            del self.books[title]
            self.save_books()
            print(f"Book ' {title}' removed.")
        else:
            print(f"Book '{title}' not found.")

    def search_book(self, title):
        """ Search for a book in the library"""
        if title in self.books:
            book = self.books[title]
            status = "Available" if book['available'] else "Not available"
            print(f"Title: {title}, Author: {book['author']}, Status: {status}")
        else:
            print(f"Book' {title}' not found. ")

    def borrow_book(self, title):
        """Borrow a book from the library"""
        if title in self.books:
            if self.books[title]['available']:
                self.books[title]['available'] = False
                self.save_books()
                print(f"You've borrowed '{title}' .")
            else:
                print(f"Book '{title}' is already borrowed. ")
        else:
            print(f"Book '{title}' not found.")

    def return_book(self, title):
        """Return a borrowed book"""
        if title in self.books:
            if not self.books[title]['available']:
                self.books[title]['available'] = True
                self.save_books()
                print(f"Book '{title}' returned.")
            else:
                print(f"Book '{title}' was not borrowed.")
        else:
            print(f"Book '{title}' not found")

    def display_books(self):
        """Display all books in the library."""
        if not self.books:
            print("The library is empty.")
            return
        print("Library Books:")
        for title, details in self.books.items():
            status = "Available" if details['available'] else "Not available"
            print(f"Title: {title}, Author: {details['author']}, Status: {status}")


# Main program loop
if __name__ == "__main__":
    library = Library()

    while True:
        print("n\Library Management System")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Search Book")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Display Book")
        print("7. Exit Book")

        choice = input("Enter your choice")

        if choice =='1':
            title = input("Enter book title:")
            author = input("Enter book title")
            library.add_book(title,author)
        elif choice == '2':
            title = input("Enter book title to remove")
            library.remove_book(title)
        elif choice == '3':
            title = input("Enter book title to search:")
            library.search_book(title)
        elif choice == '4':
            title = input("Enter book title to borrow:")
            library.borrow_book(title)
        elif choice == '5':
            title = input("Enter book title to return")
            library.return_book(title)
        elif choice == '6':
            library.display_books()
        elif choice  == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice . Please try again.")