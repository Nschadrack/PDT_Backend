
class User:
    def __init__(self, name, email, password=None):
        self.name = name
        self.email = email
        self.password_hash = password

    def set_name(self, name):
        self.name = name

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password_hash = password

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password_hash

    def __str__(self):
        return f"User: {self.name}"
