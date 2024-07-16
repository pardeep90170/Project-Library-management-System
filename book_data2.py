class Library:
    def __init__(self, name, id, stream, date,rate):
        self.book_name = name
        self.book_id = id
        self.book_stream = stream
        self.book_date = date
        self.book_rate = rate
    
    def book(self):
        print("Welcome To Library Management System In A Book Gallery....")
        book_data = {
            "name": self.book_name,
            "book_id": self.book_id,  # Ensure consistency in naming
            "book_stream": self.book_stream,
            "status": self.book_date,
            "rate": self.book_rate
        }
        return book_data
