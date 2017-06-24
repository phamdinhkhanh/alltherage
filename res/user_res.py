from flask_restful import Resource, reqparse
import mlab
from model.customer import *
from mongoengine import *
from model.rage import *
from flask import request

class ACustomer(Resource):
    def get(self, id):
        print("Get an user")
        customer = Customer.objects().with_id(id)
        return mlab.item2json(customer), 200

    def delete(self, id):
        customer = Customer.objects().with_id(id)
        customer.delete()
        return {"meassage":"OK"}, 200

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument(name="address", type=str, location="json")
        parser.add_argument(name="address_order", type = str, location ="json")
        parser.add_argument(name="username", type=str, location="json")
        parser.add_argument(name="phone_number", type=str, location="json")
        parser.add_argument(name="urlPic",type=str,location="json")
        parser.add_argument(name="urlFb",type=str,location="json")
        parser.add_argument(name="password",type=str,location="json")
        body = parser.parse_args()
        address = body.address
        address_order = body.address_order
        username = body.username
        phone_number = body.phone_number
        urlPic = body.urlPic
        urlFb = body.urlFb
        password = body.password
        customer = Customer.objects().with_id(id)
        customer.update(address=address,address_order = address_order, username=username, phone_number=phone_number,urlPic=urlPic,urlFb=urlFb,password = password)
        edit_user = Customer.objects().with_id(id)
        return mlab.item2json(edit_user), 200

class ACustomerByName(Resource):
    def get(self, id):
        print("Get an user by username")
        customer = Customer.objects(username = id).first()
        return customer.get_id(), 200

class CustomerRageLike(Resource):
    def post(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument(name="id", type=str, location="json")
        body = parser.parse_args()
        id_rage = body["id"]
        rage = Rage.objects().with_id(id_rage)
        customer = Customer.objects.with_id(id)
        rages = list(customer.rages_like)
        for rag in rages:
            if rag == rage:
                return {"message": "có rồi add cc đm"}, 401
        rages.append(rage)
        customer.update(set__rages_like=rages)
        return {"message": "ok"}, 200

    def get(self,id):
        customer=Customer.objects().with_id(id)
        return [rage.get_json() for rage in customer.rages_like]

    def delete(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument(name="id", type=str, location="json")
        body = parser.parse_args()
        id_rage = body["id"]
        try: rage = Rage.objects().with_id(id_rage)
        except:
            return {"message":"có món này đâu mà delete"}, 404
        customer = Customer.objects.with_id(id)
        rages_like = customer.rages_like

        rages_like.remove(rage)
        customer.update(set__rages_like = rages_like)
        return {"message":"OK"},200



