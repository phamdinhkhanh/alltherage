from mongoengine import *
import mlab

class GiftCode(Document):
    code=StringField()
    user_number=IntField()
    spend_min=FloatField()
    price=FloatField()

    def to_json(self):
        return {"code":self.code,
                "user_number":self.user_number,
                "spend_min":self.spend_min,
                "price":self.price
                }