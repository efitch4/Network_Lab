# Base class for People
class Person:
    def __init__(self, name, age):
        self.name = name  # Encapsulating 'name'
        self.age = age    # Encapsulating 'age'

    def get_details(self):
        return f"Name: {self.name}, Age: {self.age}"


# Derived class for Patrons (inherits from Person)
class Patron(Person):
    def __init__(self, name, age, patron_id):
        super().__init__(name, age)  # Inheriting name and age from Person class
        self.patron_id = patron_id  # Unique ID for the patron
        self.borrowed_books = []    # List to store borrowed books
    
    # Method to borrow a book
    def borrow_book(self, book):
        if book.available:
            self.borrowed_books.append(book)
            book.borrow(self.name)
            print(f"{self.name} borrowed the book '{book.title}'.")
        else:
            print(f"Sorry, the book '{book.title}' is not available.")

    # Method to return a book
    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.return_book()
            print(f"{self.name} returned the book '{book.title}'.")
        else:
            print(f"{self.name} did not borrow the book '{book.title}'.")

    # Overriding get_details method (polymorphism)
    def get_details(self):
        return f"Patron: {self.name}, ID: {self.patron_id}, Age: {self.age}, Borrowed Books: {len(self.borrowed_books)}"


# Book class (no inheritance)
class Book:
    def __init__(self, title, author, isbn):
        self.title = title        # Encapsulating 'title'
        self.author = author      # Encapsulating 'author'
        self.isbn = isbn          # Encapsulating 'isbn'
        self.available = True     # Book availability status

    # Method to borrow the book
    def borrow(self, patron_name):
        self.available = False
        print(f"'{self.title}' has been borrowed by {patron_name}.")

    # Method to return the book
    def return_book(self):
        self.available = True
        print(f"'{self.title}' has been returned and is available for borrowing.")

    # Method to get book details
    def get_details(self):
        status = "Available" if self.available else "Not Available"
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Status: {status}"


# Library class to manage books and patrons
class Library:
    def __init__(self):
        self.books = []           # Encapsulating the list of books
        self.patrons = []         # Encapsulating the list of patrons

    # Method to add a book to the library
    def add_book(self, book):
        self.books.append(book)
        print(f"Book '{book.title}' added to the library.")

    # Method to add a patron to the library
    def add_patron(self, patron):
        self.patrons.append(patron)
        print(f"Patron '{patron.name}' added to the library.")

    # Method to display all books
    def display_books(self):
        print("\nLibrary Books:")
        for book in self.books:
            print(f" - {book.get_details()}")

    # Method to display all patrons
    def display_patrons(self):
        print("\nLibrary Patrons:")
        for patron in self.patrons:
            print(f" - {patron.get_details()}")


# Example usage
if __name__ == "__main__":
    # Create a library
    library = Library()

    # Create some books
    book1 = Book("1984", "George Orwell", "9780451524935")
    book2 = Book("To Kill a Mockingbird", "Harper Lee", "9780060935467")
    book3 = Book("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")

    # Add books to the library
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)

    # Create some patrons
    patron1 = Patron("Alice", 30, "P1001")
    patron2 = Patron("Bob", 25, "P1002")

    # Add patrons to the library
    library.add_patron(patron1)
    library.add_patron(patron2)

    # Display books and patrons
    library.display_books()
    library.display_patrons()

    # Patrons borrowing books
    patron1.borrow_book(book1)
    patron2.borrow_book(book2)

    # Display books and patrons again (after borrowing)
    library.display_books()
    library.display_patrons()

    # Patrons returning books
    patron1.return_book(book1)
    patron2.return_book(book2)

    # Display books and patrons again (after returning)
    library.display_books()
    library.display_patrons()
