from models.base_model import BaseModel
import peewee as pw


class User(BaseModel):
    name = pw.CharField(null=False, unique=False)
    email = pw.CharField(null=False, unique=True)
    password = pw.CharField(null=False, unique=False)
