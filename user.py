class User:
    def __init__(self, name, id, password):
        self.name = name
        self.id = id
        self.password = password

    def matched(self, user):
        try:
            return self.id == user["id"] and self.password == user["password"]
        except TypeError:
            print("Your id or password is wrong...")
            return False

    def admin_signup(self):
        print("Signup successful in library Management System...")
        admin_data = {
            "name": self.name,
            "id": self.id,
            "isAdmin": 1,
            "password": self.password
        }
        return admin_data

    def user_signup(self):
        print("User signup successful in library Management System..")
        user_data = {
            "name": self.name,
            "id": self.id,
            "isUser": 1,
            "password": self.password
        }
        return user_data
