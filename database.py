import pymongo

try:
    client = pymongo.MongoClient("mongodb://localhost:27017")
    print("Connected to MongoDB")

    # Access the database
    db = client['Library_Management_System']

    # Collection of users
    user_collection = db['users']
    admin_collection = db['admin']
    book_collection = db['books']
    course_stream_collection = db["course_stream"]
except Exception as e:
    print("Failed to connect to MongoDB", e)
    user_collection = None
    admin_collection = None
    book_collection = None
    course_stream_collection = None
