    
class Library:
    def __init__(self,name,id,stream,date):
        self.book_name=name
        self.book_id=id
        self.book_stream=stream
        self.book_date = date
    
    
    def book(self):
        print("Weclome To Library Managment System In A Book Gallery....")
        book_data = {
            "name": self.book_name,
            "id": self.book_id,
            "stream": self.book_stream,
            "status": self.book_date
        } 
        return book_data               


    
    