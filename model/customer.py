from mongoengine import *
import mlab
class Customer(Document):
    username = StringField();
    password = StringField();
    token = StringField();
    id_user = StringField();
    address = StringField();
    address_order = StringField();
    day = StringField();
    month = StringField();
    year = StringField();
    birth_day = StringField();
    phone_number = StringField();
    total_spend = FloatField();
    oid = StringField();
    urlPic = StringField();
    urlFb = StringField();
    email = StringField();
    rages_like = ListField(ReferenceField("Rage"));
    comment = ListField(ReferenceField("Comment"))

    def get_json(self):
        str = mlab.item2json(self)
        oid = str["_id"]["$oid"]
        return {
            "id_system":oid,
            "id_user":self.id_user,
            "username": self.username,
            "password":self.password,
            "token":self.token,
            "address":self.address,
            "address_order":self.address_order,
            "birth_day":self.birth_day,
            "phone_number":self.phone_number,
            "total_spend":self.total_spend,
            "oid":self.oid,
            "urlPic":self.urlPic,
            "urlFb":self.urlFb,
            "email":self.email,
            "rages_like":self.rages_like,
            "comment":self.comment
        }

    def get_id(self):
        str = mlab.item2json(self)
        oid = str["_id"]["$oid"]
        return {
            "$oid":oid
        }

