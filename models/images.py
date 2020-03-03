from models.base_model import BaseModel
import peewee as pw
from models.user import User
from playhouse.hybrid import hybrid_property


class Image(BaseModel):
    user = pw.ForeignKeyField(User, backref='images')
    user_img = pw.CharField(null=True)
    caption = pw.CharField(null=True)

    @hybrid_property
    def user_image_url(self):
        return(f'https://nextagram-jordan.s3.amazonaws.com/{self.user_img}')

    @hybrid_property
    def total_donation(self):
        from models.donations import Donations
        total = 0
        for donation in self.donations:
            total += donation.amount

        return total
