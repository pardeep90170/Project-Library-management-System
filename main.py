from user import User
from book_data2 import Library
from database import user_collection, admin_collection, book_collection, course_stream_collection
import re
from datetime import datetime, timedelta
import uuid  # Import the uuid module

# Dictionary to store unique IDs and corresponding names
unique_ids = {}

admin_logged_in = False  # Initialize admin_logged_in variable

#  Admin function for signup to create an account
def admin():
    print("Welcome to signup page for Admin..")
    name = input("Enter your name:")
    id = input("Enter your email id:")

    if id not in unique_ids:  # Check if the ID is unique
        unique_ids[id] = name  # Store the ID and name
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
    else:
        print("This email id is already registered.")
# Matching user and admin email and password
def matching(name, id, password):
    id_pattern = r'^[\w\.-]+@(gmail\.com|outlook\.com|hotmail\.com)$'
    password_pattern = r'^.{5,}$'
    if not re.match(id_pattern, id) or not re.match(password_pattern, password):
        return "invalid"
    else:
        return "matching"

# User function for signup to create an account
def user():
    print("Welcome to signup page..")
    name = input("Enter your name:")
    id = input("Enter your email email id:")
    
    if id not in unique_ids:  # Check if the ID is unique
        unique_ids[id] = name  # Store the ID and name
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
    else:
        print("This email id is already registered.")

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
        return id  # Return user ID if login is successful
    else:
        print("Invalid email or password.")
        return None
# Admin function to log in to the account
def admin_Login():
    global admin_logged_in  # Use global keyword to modify admin_logged_in variable
    print("Welcome to admin login page..")
    id = input("Enter your email id:")
    password = input("Enter your password:")
    found_user_admin_data = admin_collection.find_one({"id": id, "password": password})
    admin_login = User("", id, password)
    y = admin_login.matched(found_user_admin_data)
    if y:
        global admin_id  # Define global variable to store admin ID
        admin_id = id  # Store admin ID when logged in
        print("Welcome To Admin DashBoard....")
        admin_logged_in = True  # Update admin_logged_in when admin logs in


#  this function use in ramdom id generate
def generate_random_id():
    return uuid.uuid4().hex[:6]  # Generate a random ID and return the first 6 characters

# this function use in add book
def add_book():
    print("Book Adding In Library Management System....")
    try:
        book_name = input("Enter the name of the book:")
        book_id = generate_random_id()
        book_stream = input("Enter the book stream:")
        book_rate = float(input("Enter the book rate: "))  # Add the book rate input
        # Capture the current date and time
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        added_book_data = Library(book_name, book_id, book_stream, current_date, book_rate)  # Use the current date and book rate
        insert_book_data = added_book_data.book()
        book_collection.insert_one(insert_book_data)
        print("Book Added successfully....")
    except ValueError:
        print("Invalid input. Please enter a valid book ID.")
    except Exception as e:
        print("An error occurred:", str(e))

# function to issue a book
def issue_book(admin_name):
    print("Issue Book in Library Management System....")
    try:
        user_name = input("Enter the user name: ")
        book_name = input("Enter the name of the book you want to issue: ")
        print(book_name)
        
        # Check if the book is available in the library
        book = book_collection.find_one({"name": book_name})
        if book:
            issued_to = book.get("issued_to")
            book_stream = book.get("book_stream")  # Get the book_stream attribute
            
            # Ensure the book has an id field
            if "id" not in book:
                book_id = str(book["_id"])  # Assuming MongoDB auto-generates _id
                book_collection.update_one({"name": book_name}, {"$set": {"id": book_id}})
                book["id"] = book_id
            else:
                book_id = book["id"]
            
            if issued_to is None:
                issue_date = datetime.now().strftime("%Y-%m-%d")
                return_date = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
                
                if book_stream:
                    print(f"Book details: book_id: {book_id}, name: {book_name}, Stream: {book_stream}")
                else:
                    print(f"Book details: book_id: {book_id}, name: {book_name}, Stream information not available")
                
                # Update the book status to indicate it's issued to the user
                book_collection.update_one(
                    {"name": book_name},
                    {"$set": {"issued_to": user_name, "issued_by": admin_name, "issue_date": issue_date, "return_date": return_date}}
                )
                print(f"Book '{book_name}' has been issued to user {user_name} by admin {admin_name}.")
                print(f"Issue Date: {issue_date}, Return Date: {return_date}")
            else:
                print(f"Book '{book_name}' is already issued to user {issued_to}.")
        else:
            print(f"No book found with the name '{book_name}'")
    except Exception as e:
        print("An error occurred:", str(e))

# function to return a book
def return_book():
    print("Return Book in Library Management System....")
    try:
        user_name = input("Enter your name: ")
        book_name = input("Enter the name of the book you want to return: ")
        print(book_name)
        
        # Check if the book is issued to the user
        book = book_collection.find_one({"name": book_name, "issued_to": user_name})
        if book:
            # Calculate the fine if the book is overdue
            return_date = datetime.strptime(book["return_date"], "%Y-%m-%d")
            current_date = datetime.now()
            if current_date > return_date:
                overdue_days = (current_date - return_date).days
                fine_amount = overdue_days * 50  # 50 rupees per day
                print(f"The book is overdue by {overdue_days} days. The fine is {fine_amount} rupees.")
            else:
                fine_amount = 0
                print("The book is returned on time. No fine.")
            
            # Update the book status to indicate it's returned
            book_collection.update_one(
                {"name": book_name},
                {"$unset": {"issued_to": "", "issued_by": "", "issue_date": "", "return_date": ""}}
            )
            print(f"Book '{book_name}' has been returned by user {user_name}. Fine amount: {fine_amount} rupees.")
        else:
            print(f"No record found for book '{book_name}' issued to user {user_name}.")
    except Exception as e:
        print("An error occurred:", str(e))

# function to extend the return date of a book
def extend_return_date():
    print("Extend Return Date in Library Management System....")
    try:
        user_name = input("Enter your name: ")
        book_name = input("Enter the name of the book for which you want to extend the return date: ")
        print(book_name)
        
        # Check if the book is issued to the user
        book = book_collection.find_one({"name": book_name, "issued_to": user_name})
        if book:
            new_return_date = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
            book_collection.update_one(
                {"name": book_name},
                {"$set": {"return_date": new_return_date}}
            )
            print(f"The return date for book '{book_name}' has been extended by 15 days. New return date: {new_return_date}")
        else:
            print(f"No record found for book '{book_name}' issued to user {user_name}.")
    except Exception as e:
        print("An error occurred:", str(e))

# Function for book searching
def searching_book():
    print("Searching for a book...")
    try:
        book_name = input("Enter the name of the book: ")

        # Use aggregation to find and count books in a single query
        pipeline = [
            {"$match": {"name": book_name}},
            {"$project": {"book_id": {"$ifNull": ["$book_id", "N/A"]}, "name": 1, "book_stream": {"$ifNull": ["$book_stream", "N/A"]}}},
            {"$group": {"_id": None, "count": {"$sum": 1}, "books": {"$push": "$$ROOT"}}}
        ]

        results = list(book_collection.aggregate(pipeline))

        if results and results[0]["count"] > 0:
            num_books = results[0]["count"]
            found_books = results[0]["books"]
            print(f"Number of books found: {num_books}")

            for book in found_books:
                book_id = book.get('book_id', 'N/A')  # Use 'N/A' if book_id is missing
                book_name = book.get('name', 'N/A')
                book_stream = book.get('book_stream', 'N/A')
                print(f"Book ID: {book_id}, Book Name: {book_name}, Stream: {book_stream}")
        else:
            print("No books found matching the search criteria.")
    except Exception as e:
        print("An error occurred:", str(e))

# Function to get a list of all books
def list_all_books():
    print("Listing all books in the Library Management System...")
    try:
        books = book_collection.find({})
        if books:
            for book in books:
                book_id = book.get('book_id', 'N/A')
                book_name = book.get('name', 'N/A')
                book_stream = book.get('book_stream', 'N/A')
                issued_to = book.get('issued_to', 'Not Issued')
                issue_date = book.get('issue_date', 'N/A')
                return_date = book.get('return_date', 'N/A')
                print(f"Book ID: {book_id}, Book Name: {book_name}, Stream: {book_stream}, Issued To: {issued_to}, Issue Date: {issue_date}, Return Date: {return_date}")
        else:
            print("No books found in the library.")
    except Exception as e:
        print("An error occurred:", str(e))

# function to calculate fine for lost book
def calculate_lost_book_fine():
    print("Calculate Fine for Lost Book in Library Management System....")
    try:
        user_name = input("Enter your user_name: ")
        book_name = input("Enter the name of the book you lost: ")
        print(book_name)
        
        # Check if the book is issued to the user
        book = book_collection.find_one({"name": book_name, "issued_to": user_name})
        if book:
            book_rate = book.get("book_rate", 0)  # Get the book rate, default to 0 if not found
            print(f"The fine for the lost book '{book_name}' is {book_rate} rupees.")
        else:
            print(f"No record found for book '{book_name}' issued to user {user_name}.")
    except Exception as e:
        print("An error occurred:", str(e))

# Function to borrow a book
def borrow_book(user_id):
    print("Borrowing a book...")
    try:
        # Check if the user has already borrowed a book
        user_borrowed_books = book_collection.find({"issued_to": user_id})
        num_borrowed_books = len(list(user_borrowed_books))
        if num_borrowed_books >= 1:
            print(f"User {user_id} already has a borrowed book. You cannot borrow more than one book at a time.")
            return
        
        book_name = input("Enter the name of the book you want to borrow: ")
        book = book_collection.find_one({"name": book_name})
        
        if book:
            if book.get("issued_to") is None:
                book_collection.update_one({"name": book_name}, {"$set": {"issued_to": user_id}})
                print(f"Book '{book_name}' has been borrowed by user {user_id}.")
            else:
                print(f"Book '{book_name}' is already issued.")
        else:
            print(f"No book found with the name '{book_name}'.")
    except Exception as e:
        print("An error occurred:", str(e))

# Function to view borrowed books
def view_borrowed_books(user_id):
    print("Viewing borrowed books...")
    try:
        user = user_collection.find_one({"id": user_id})
        if user:
            user_email = user.get("id")
            borrowed_books = book_collection.find({"issued_to": user_id})
            borrowed_books_list = list(borrowed_books)
            if borrowed_books_list:
                print(f"User {user_email} has borrowed the following books:")  
                for book in borrowed_books_list:
                    print(f"ID: {book['id']}, Title: {book['name']}")
            else:
                print(f"User {user_email} has not borrowed any books.")
        else:
            print(f"No user found with ID '{user_id}'.")
    except Exception as e:
        print("An error occurred:", str(e))

        # Function to delete a book from the library
def delete_book():
    print("Deleting a book from the Library Management System...")
    try:
        book_name = input("Enter the name of the book you want to delete: ")

        # Check if the book exists in the library
        book = book_collection.find_one({"name": book_name})

        if book:
            book_collection.delete_one({"name": book_name})
            print(f"Book '{book_name}' has been deleted from the library.")
        else:
            print(f"No book found with the name '{book_name}' in the library.")
    except Exception as e:
        print("An error occurred:", str(e))

# Function to delete in user account details in library managment system
def delete_user_account():
    print("Deleting a user account...")
    try:
        user_email = input("Enter the email ID of the user whose account you want to delete: ")

        # Check if the user exists in the collection
        user = user_collection.find_one({"id": user_email})

        if user:
            user_collection.delete_one({"id": user_email})
            print(f"User account with email '{user_email}' has been successfully deleted.")
        else:
            print(f"No user account found with email '{user_email}'.")
    except Exception as e:
        print("An error occurred:", str(e))

def logout_account():
    global admin_logged_in
    print("Logging out admin...")
    admin_logged_in = False
    print("Admin logged out successfully.")

# Main program logic
if __name__ == "__main__":
    print("\t\t\t\t-------WELCOME TO LIBRARY MANAGEMENT SYSTEM-------\t")
    print("======================================="*3)
    print("Press 1 for library System")
    print("Press 2 for exiting the library")
    print("======================================="*3)

    choice = int(input("Enter your choice (1-2): "))
    if choice == 1:
        # Login page
        while True:
            try:
                print("======================================="*3)
                print("Press 1 for admin signup")
                print("Press 2 for user signup")
                print("Press 3 for user login")
                print("Press 4 for admin login")
                print("Press 5 for exiting")
                print("======================================="*3)
                login_choice = int(input("Enter your choice (1-5): "))
                if login_choice == 1:
                    admin()
                elif login_choice == 2:
                    user()
                elif login_choice == 3:
                    user_id = user_Login()
                    if user_id:
                        while True:
                            print("======================================="*3)
                            print("Press 1 to Search Books")
                            print("Press 2 to Borrow Books")
                            print("Press 3 to View Borrowed Books")
                            print("Press 4 to Logout")
                            print("======================================="*3)
                            user_option = int(input("Enter your choice (1-4): "))
                            if user_option == 1:
                                searching_book()
                            elif user_option == 2:
                                borrow_book(user_id)                        
                            elif user_option == 3:
                                view_borrowed_books(user_id)
                            elif user_option == 4:
                                print("LogOut the ID...")
                                break
                            else:
                                print("Invalid choice. Please enter a number between 1 and 5.")
                elif login_choice == 4:
                    admin_Login()
                    if admin_logged_in:
                        while True:
                            print("======================================="*3)
                            print("Press 1 Add Book")
                            print("Press 2 Issue Book")
                            print("Press 3 Retrun of Book and Fine of due book of date")
                            print("Press 4 Extend of Book date")
                            print("Press 5 Searching For Book In Library")
                            print("Press 6 List of all books")
                            print("Press 7 Lost of book fine")
                            print("Press 8 Delete In User Account")
                            print("Press 9 Delete Book In Library Management System")
                            print("Press 10 Exit the Admin Menu")
                            print("Press 11 Logout In Admin Account")
                            print("======================================="*3)
                            admin_option = int(input("Enter your choice (1-11): "))
                            if admin_option == 1:
                                add_book()
                            elif admin_option == 2:
                                issue_book(admin_id)
                            elif admin_option == 3:
                                return_book()
                            elif admin_option == 4:
                                extend_return_date()  
                            elif admin_option == 5:
                                searching_book()
                            elif admin_option == 6:
                                list_all_books()
                            elif admin_option == 7:
                                calculate_lost_book_fine()
                            elif admin_option == 8:
                                delete_user_account()
                            elif admin_option == 9:
                                delete_book()
                            elif admin_option == 10:
                                print("Exiting admin menu...")
                                break
                            elif admin_option == 11:
                                logout_account()
                                break
                            else:
                                print("Invalid choice. Please enter a number between 1 and 8.")
                elif login_choice == 5:
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    elif choice == 2:
        print("Exiting...")
    else:
        print("Invalid choice. Please enter a number between 1 and 2.")