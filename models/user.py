from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash


class User(BaseModel):
    name = pw.CharField(null=False, unique=True)
    email = pw.CharField(null=False, unique=True)
    password = pw.CharField(null=False, unique=False)

    def validate(self):
        duplicate_username = User.get_or_none(User.name == self.name)
        duplicate_email = User.get_or_none(User.email == self.email)
        string_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if duplicate_username:
            self.errors.append('username is taken!')
        if duplicate_email:
            self.errors.append(
                'email address is associated with another account!')
        if "@" not in self.email:
            self.errors.append('please enter a valid email')
        if (string_check.search(self.password) == None):
            self.errors.append(
                'password must contain at least one special character')
        if len(self.password) <= 6:
            self.errors.append('password has to be more than 6 characters')
        if self.password.isupper() or self.password.islower():
            self.errors.append(
                'password must be a combination of upper and lower case characters')
        else:
            self.password = generate_password_hash(self.password)
