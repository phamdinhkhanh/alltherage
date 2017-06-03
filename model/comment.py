from mongoengine  import *
import mlab
from model.customer import *
from model.rage import *


class Comment(Document):
    customer=ReferenceField("Customer")
    message=StringField()
    rage=ReferenceField("Rage")
    date=StringField()

    def get_json(self):
        str=mlab.item2json(self)
        oid=str["_id"]["$oid"]
        return {
            "id_comment":oid,
            "customer":self.customer.get_json(),
            "message":self.message,
            "rage":self.rage.get_json(),
            "date":self.date
        }