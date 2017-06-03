from mongoengine import *
from flask_restful import Resource, reqparse
import mlab

class Rage(Document):
    name = StringField();
    url = StringField();
    description = StringField();
    old_price = FloatField();
    new_price = FloatField();
    discount_rate = FloatField();
    is_favorite = BooleanField();

    def get_json(self):
        return mlab.item2json(self)



class RageInfo(Document):
    rage = ReferenceField("Rage");
    info = StringField();

    def get_json(self):
        return {
            "food":self.rage.get_json(),
            "info":self.info
        }
