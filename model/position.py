from mongoengine import *
import mlab
from model.customer import *
from model.rage import *


class Position(Document):
    name = StringField();
    url = StringField();
    website = StringField();
    address = StringField();
    description = StringField();
    opentime = StringField();
    phone = StringField();
    latitude = StringField();
    longtitude = StringField();
    number_seen = IntField();
    code =StringField();
    rating = FloatField();
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
            "customer":self.customer.get_json()
        }

