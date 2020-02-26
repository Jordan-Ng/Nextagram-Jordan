import os
import peewee as pw
import datetime
from database import db


class BaseModel(pw.Model):
    created_at = pw.DateTimeField(default=datetime.datetime.now)
    updated_at = pw.DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.errors = []
        self.validate()

        if len(self.errors) == 0:
            self.updated_at = datetime.datetime.now()
            return super(BaseModel, self).save(*args, **kwargs)
        else:
            return 0

    def validate(self):
        from models.user import User
        import re
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
        if(string_check.search(self.password) == None):
            self.errors.append(
                'password must contain at least one special character')
        if len(self.password) <= 6:
            self.errors.append('password has to be more than 6 characters')
        if self.password.isupper() or self.password.islower():
            self.errors.append(
                'password must be a combination of upper and lower case characters')
        # print(
        #     f"Warning validation method not implemented for {str(type(self))}")
        # return True

    class Meta:
        database = db
        legacy_table_names = False
