from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from playhouse.hybrid import hybrid_property


class User(BaseModel):
    name = pw.CharField(null=False, unique=True)
    email = pw.CharField(null=False, unique=True)
    password = pw.CharField(null=False, unique=False)
    profile_image = pw.CharField(null=True)

    def validate(self):
        duplicate_username = User.get_or_none(User.name == self.name)

        duplicate_email = User.get_or_none(User.email == self.email)

        string_check = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        if duplicate_username and not duplicate_username.id:
            self.errors.append('username is taken!')

        if duplicate_email and not duplicate_email.id:
            self.errors.append(
                'email address is associated with another account!')

        if "@" not in self.email:
            self.errors.append('please enter a valid email')

        # if not self.id and (string_check.search(self.password) == None):
        #     self.errors.append(
        #         'password must contain at least one special character')
        if not self.id and len(self.password) <= 6:
            self.errors.append('password has to be more than 6 characters')
        if not self.id and self.password.isupper():
            self.errors.append('Password must have upper case.')
        if not self.id and self.password.islower():
            self.errors.append(
                'Password must have lower case')
        else:
            if not self.id:
                self.password = generate_password_hash(self.password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    @hybrid_property
    def prof_image_url(self):
        return(f'https://nextagram-jordan.s3.amazonaws.com/{self.profile_image}')
