from mongoengine import *
import mlab
from model.customer import *


class Position(Document):
    name = StringField();
    url = StringField();
    website = StringField();
    address = StringField();
    description = StringField();
    opentime = StringField();
    phone = StringField();
    latitude = FloatField();
    longtitude = FloatField();
    number_seen = IntField();
    code =StringField();
    rating = FloatField();
    number_rating = IntField();
    customer = ReferenceField("Customer");

    def get_json(self):
        str=mlab.item2json(self)
        oid=str["_id"]["$oid"]
        return {
            "oid":oid,
            "name":self.name,
            "url":self.url,
            "website":self.website,
            "address":self.address,
            "description":self.description,
            "opentime":self.opentime,
            "phone":self.phone,
            "latitude": self.latitude,
            "longtitude":self.longtitude,
            "number_seen":self.number_seen,
            "code":self.code,
            "rating":self.rating,
            "number_rating":self.number_rating,
            "customer":self.customer.get_json_oid()
        }

    def get_json_oid(self):
        str=mlab.item2json(self)
        oid=str["_id"]["$oid"]
        return {
            "oid":oid
        }
