# from data import myvariable


# class create
class User:
    def __init__(self, name, id, password):
        self.name = name
        self.id = id
        self.password = password
        

    # matched function
    def matched(self, user):
        # return self.id == user["id"] and self.password == user["password"]
        try:
            return self.id == user["id"] and self.password == user["password"]
        except TypeError:
            print("Your id or password is wrong...")



# admin login fucntion
    def admin_signup(self):
        print("Signup To sucessfully in library Management System...")
        admin_data = {
            "name": self.name,
            "id": self.id,
            "isAdmin": 1,
            "isAdmin":0,
            "password": self.password           
        }
        return admin_data
   
    def user_signup(self):
        print("User To successfully in library Management System..")
        user_data = {
            "name": self.name,
            "id": self.id,
            "isUser": 1,
            "isUser":0,
            "password": self.password
            
        }
        return  user_data
