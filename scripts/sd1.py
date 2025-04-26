import sqlite3 

# SQL-Python Basics Code

# Step 1: Connect to or create the SQLite database
def create_connection():
    conn = sqlite3.connect('basics_sql_python.db')
    return conn

# Step 2: Create a table if it doesn't exist
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER,
                        email TEXT UNIQUE NOT NULL)''')
    conn.commit()

# Step 3: Insert a new user into the table
def insert_user(conn, name, age, email):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", (name, age, email))
        conn.commit()
        print(f"User {name} added successfully!")
    except sqlite3.IntegrityError:
        print(f"Error: A user with the email {email} already exists.")

# Step 4: Query and fetch all users
def fetch_all_users(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No users found.")

# Step 5: Update a user's email
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    conn.commit()
    if cursor.rowcount:
        print(f"User ID {user_id}'s email updated successfully to {new_email}.")
    else:
        print(f"No user found with ID {user_id}.")

# Step 6: Delete a user by ID
def delete_user(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    if cursor.rowcount:
        print(f"User ID {user_id} deleted successfully.")
    else:
        print(f"No user found with ID {user_id}.")

# Step 7: User interaction: Add, view, update, or delete users
def user_menu(conn):
    while True:
        print("\n--- SQL-Python Basics ---")
        print("1. Add User")
        print("2. View All Users")
        print("3. Update User Email")
        print("4. Delete User")
        print("5. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            name = input("Enter user name: ")
            age = int(input("Enter user age: "))
            email = input("Enter user email: ")
            insert_user(conn, name, age, email)
        
        elif choice == '2':
            print("\nFetching all users...")
            fetch_all_users(conn)
        
        elif choice == '3':
            user_id = int(input("Enter the User ID to update: "))
            new_email = input("Enter the new email: ")
            update_user_email(conn, user_id, new_email)
        
        elif choice == '4':
            user_id = int(input("Enter the User ID to delete: "))
            delete_user(conn, user_id)
        
        elif choice == '5':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid option. Please try again.")

# Main program execution
def main():
    # Step 1: Connect to database
    conn = create_connection()
    
    # Step 2: Create table
    create_table(conn)
    
    # Step 3: Run user menu to interact with the database
    user_menu(conn)
    
    # Step 4: Close connection when done
    conn.close()

if __name__ == "__main__":
    main() 
