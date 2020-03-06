import peewee as pw
from models.base_model import BaseModel
from models.user import User
from models.images import Image
from playhouse.hybrid import hybrid_property


class Donations(BaseModel):
    amount = pw.DecimalField()
    image = pw.ForeignKeyField(Image, backref="donations")
    user = pw.ForeignKeyField(User, backref="donations")
