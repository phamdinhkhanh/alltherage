from mongoengine import *
import mlab
class Customer(Document):
    username = StringField();
    password = StringField();
    token = StringField();
    mamay = StringField();
    username_show = StringField();
    address = StringField();
    address_order = StringField();
    day = StringField();
    month = StringField();
    year = StringField();
    birth_day = StringField();
    phone_number = StringField();
    total_spend = FloatField();
    urlPicEmail = StringField();
    urlPicFb = StringField();
    urlFb = StringField();
    email = StringField();
    rages_like = ListField(ReferenceField("Rage"));
    comment = ListField(ReferenceField("Comment"));
    type_account = StringField();

    def get_json(self):
        str = mlab.item2json(self)
        oid = str["_id"]["$oid"]
        return {
            "oid":oid,
            "username_show":self.username_show,
            "username": self.username,
            "password":self.password,
            "token":self.token,
            "mamay":self.mamay,
            "address":self.address,
            "address_order":self.address_order,
            "birth_day":self.birth_day,
            "phone_number":self.phone_number,
            "total_spend":self.total_spend,
            "urlPicEmail":self.urlPicEmail,
            "urlPicFb":self.urlPicFb,
            "urlFb":self.urlFb,
            "email":self.email,
            "rages_like":self.rages_like,
            "comment":self.comment,
            "type_account":self.type_account
        }


    def get_id(self):
        str = mlab.item2json(self)
        oid = str["_id"]["$oid"]
        return {
            "oid":oid
        }

    def get_avatar(self):
        str = mlab.item2json(self)
        oid = str["_id"]["$oid"]
        return {
            "oid":oid,
            "username_show":self.username_show,
            "urlPicFb":self.urlPicFb,
            "urlPicEmail": self.urlPicEmail
        }