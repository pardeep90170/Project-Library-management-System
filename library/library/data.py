import pymongo
try:
    client = pymongo.MongoClient("mongodb://localhost:27017")
    print("Connected to MongoDB")

    # Access the database
    db = client['Library_Management_System']
    print(db)

    # Collection of users
    user_collection = db['users']
    print("User collection created:", user_collection)
    
    admin_collection = db['admin']
    print("User collection created:", admin_collection)
    
    book_collection = db['add_book']
    print("Book collection created:",book_collection)
    
    course_stream_collection =db["course_stream"]
    print("Course stream created",course_stream_collection)
except Exception as e:
    print("Failed to connect to MongoDB", e)
    user_collection = None

