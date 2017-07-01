from mongoengine  import *
import mlab
from model.customer import *
from model.rage import *


class Comment(Document):
    customer=ReferenceField("Customer")
    message=StringField()
    rage=ReferenceField("Rage")
    date=StringField()
    numberlike=IntField()

    def get_json(self):
        str=mlab.item2json(self)
        oid=str["_id"]["$oid"]
        return {
            "oid":oid,
            "customer":self.customer.get_avatar(),
            "message":self.message,
            "rage":self.rage.get_oid(),
            "date":self.date,
            "numberlike":self.numberlike
        }

    def get_json_norage(self):
        str=mlab.item2json(self)
        oid=str["_id"]["$oid"]
        return {
            "oid":oid,
            "customer":self.customer.get_id(),
            "message":self.message,
            "date":self.date,
            "numberlike":self.numberlike
        }