from mongoengine import *
from model.rage import Rage
import mlab
from model.customer import *


class SingleOrder(EmbeddedDocument):
    rage = ReferenceField("Rage")
    count = IntField()

    def get_json(self):
        return {
            "rage":Rage.objects().with_id(self.rage.id).get_json(),
            "count":self.count
        }

class Order(Document):
    items = ListField(EmbeddedDocumentField("SingleOrder"))
    date = StringField()
    address_order = StringField()
    phone_number = StringField()
    customer = ReferenceField("Customer")
    is_Success = BooleanField()
    spend = FloatField()
    ship_money = FloatField()
    code = StringField()
    code_price = FloatField()

    def get_json(self):
        str = mlab.item2json(self)
        oid = str["_id"]["$oid"]
        return {
            "id":oid,
            "items":[item.get_json() for item in self.items],
            "spend":self.spend,
            "date":self.date,
            "address_order":self.address_order,
            "phone_number":self.phone_number,
            "customer":self.customer.get_json(),
            "is_Success":self.is_Success,
            "ship_money":self.ship_money,
            "code":self.code,
            "code_price":self.code_price
        }

    def get_singleOrders(self):
        str = mlab.item2json(self)
        oid = str["_id"]["$oid"]
        return {
             "id":oid,
             "items": [item.get_json() for item in self.items]
        }