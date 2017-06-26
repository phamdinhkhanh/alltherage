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

    def get_oid(self):
        str = mlab.item2json(self)
        oid = str["_id"]["$oid"]
        return {
            "$oid":oid
        }

    def get_json_oid(self):
        str = mlab.item2json(self)
        oid = str["_id"]["$oid"]
        return {
           "oid": oid,
           "name": self.name,
           "url": self.url,
           "description": self.description,
           "old_price": self.old_price,
           "new_price": self.new_price,
           "discount_rate": self.discount_rate,
           "is_favorite": self.is_favorite
        }




class RageInfo(Document):
    rage = ReferenceField("Rage");
    info = StringField();

    def get_json(self):
        return {
            "rage":self.rage.get_json(),
            "info":self.info
        }
