from login import User
from book_data import Library
from data import user_collection, admin_collection, book_collection, course_stream_collection
import re

#  Admin function for signup to create an account
def admin():
    print("Welcome to signup page for Admin..")
    name = input("Enter your name:")
    id = input("Enter your email id:")
    password = input("Enter your password:")
    matched = matching(name, id, password)
    if matched == "matching":
        print("Matching successfully for admin page..")
        admin_data = User(name, id, password)
        myData = admin_data.admin_signup()
        admin_collection.insert_one(myData)
        print("Admin signup successful.")
    else:
        print("Invalid email address or password. Please enter a valid email address and password.")

# Matching user and admin email and password
def matching(name, id, password):
    id_pattern = r'^[\w\.-]+@(gmail\.com|outlook\.com|hotmail\.com)$'
    password_pattern = r'^.{8,}$'
    if not re.match(id_pattern, id) or not re.match(password_pattern, password):
        return "invalid"
    else:
        return "matching"

# User function for signup to create an account
def user():
    print("Welcome to signup page..")
    name = input("Enter your name:")
    id = input("Enter your email email id:")
    password = input("Enter your password:")
    matched = matching(name, id, password)
    if matched == "matching":
        print("Matching successfully for user page..")
        user = User(name, id, password)
        myData = user.user_signup()
        user_collection.insert_one(myData)
        print("User signup successful.")
    else:
        print("Invalid email address or password. Please enter a valid email address and Password.")

# User function to log in to the account
def user_Login():
    print("Welcome to login page User...")
    id = input("Enter your email id:")
    password = input("Enter your password:")
    found_user_data = user_collection.find_one({"id": id, "password": password})
    user_login = User("", id, password)
    x = user_login.matched(found_user_data)
    if x:
        print("Welcome To User DashBoard....")

# Admin function to log in to the account
def admin_Login():
    print("Welcome to admin login page..")
    id = input("Enter your email id:")
    password = input("Enter your password:")
    found_user_admin_data = admin_collection.find_one({"id": id, "password": password})
    admin_login = User("", id, password)
    y = admin_login.matched(found_user_admin_data)
    if y:
        print("Welcome To Admin DashBoard....")

# Function to add book data
def add_book():
    print("Book Adding In Library Management System....")
    try:
        book_name = input("Enter your name:")
        book_id = int(input("Enter your book id:"))
        book_stream = input("Enter your stream book:")
        added_book_data = Library(book_name, book_id, book_stream)
        insert_book_data = added_book_data.book()
        book_collection.insert_one(insert_book_data)
        print("Book Added successfully....")
    except ValueError:
        # Handle invalid input for book ID
        print("Invalid input. Please enter a valid book ID.")
    except Exception as e:
        # Handle any other unexpected errors
        print("An error occurred:", str(e))

# Function to issue a book
def issue_book():
    print("Issue Book in Library Management System....")
    # Implementation code goes here

# Function to check book due dates
def check_due_date():
    print("Check Date Book Issue...")
    try:
        book_id = int(input("Enter the book ID: "))
        book = book_collection.find_one({"book_id": book_id})
        if book:
            due_date = book.get("due_date")
            if due_date:
                print(f"Due date for Book ID {book_id} is {due_date}")
            else:
                print(f"No due date found for Book ID {book_id}")
        else:
            print(f"No book found with ID {book_id}")
    except ValueError:
        print("Invalid input. Please enter a valid book ID.")

# Function for book searching
def searching_book():
    print("Searching for a book...")
    try:
        book_name = input("Enter the name of the book: ")
        found_books = book_collection.find({"book_name": {"$regex": book_name, "$options": "i"}})
        if found_books.count() > 0:
            print("Found books matching the search criteria:")
            for book in found_books:
                print(f"Book ID: {book['book_id']}, Book Name: {book['book_name']}, Stream: {book
['book_stream']}")
        else:
            print("No books found matching the search criteria.")
    except Exception as e:
        print("An error occurred:", str(e))

# Main program logic
if __name__ == "__main__":
    print("-------WELCOME TO LIBRARY MANAGEMENT SYSTEM-------")
    print("Press 1 for login")
    print("Press 2 for adding a book")
    print("Press 3 for checking book due date")
    print("Press 4 for searching for a book")
    print("Press 5 for exiting the library")

    choice = int(input("Enter your choice (1-5): "))
    if choice == 1:
        # Login page
        while True:
            try:
                print("Press 1 for admin signup")
                print("Press 2 for user signup")
                print("Press 3 for user login")
                print("Press 4 for admin login")
                print("Press 5 for exiting")
                login_choice = int(input("Enter your choice (1-5): "))
                if login_choice == 1:
                    admin()
                elif login_choice == 2:
                    user()
                elif login_choice == 3:
                    user_Login()
                elif login_choice == 4:
                    admin_Login()
                elif login_choice == 5:
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    elif choice == 2:
        add_book()

    elif choice == 3:
        check_due_date()

    elif choice == 4:
        searching_book()

    elif choice == 5:
        print("Exiting...")

    else:
        print("Invalid choice. Please enter a number between 1 and 5.")
