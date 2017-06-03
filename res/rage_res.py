from mongoengine import Document, StringField
from flask_restful import Resource, reqparse
import mlab
from model.rage import *

class RageRes(Resource):
    def get(self):
        rage = Rage.objects()
        return mlab.list2json(rage), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="name", type=str, location="json")
        parser.add_argument(name="url", type=str, location="json")
        parser.add_argument(name="description", type=str, location="json")
        parser.add_argument(name="old_price", type=float, location="json")
        parser.add_argument(name="new_price", type=float, location="json")

        body = parser.parse_args()
        name = body.name
        url = body.url
        description = body.description
        try:
            old_price = float(body.old_price)
            new_price = float(body.new_price)
        except:
            return {"message": "post cái lol gì? giá là số ok? bỏ chữ Đ hay VND đi"}, 401
        discount_rate = 1-body.new_price/body.old_price

        if name is None or description is None or url is None or new_price is None or old_price is None:
            return {"message": "Gửi cc thiếu trường đcm"}, 401

        found_rage = Rage.objects(name = name).first()
        if found_rage is not None:
            return {"message":"Rage already exist"}, 401

        rage = Rage(name=name, url=url, description = description, old_price = old_price,new_price =new_price, discount_rate=discount_rate, is_favorite = False)
        rage.save()

        add_rage = Rage.objects().with_id(rage.id)
        return mlab.item2json(add_rage), 200

class ARageRes(Resource):
    def get(self,id):
        rage = Rage.objects().with_id(id)
        return mlab.item2json(rage), 200

    def delete(self,id):
        rage = Rage.objects().with_id(id)
        rage.delete()
        return {"message":"OK"},200


    def put(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument(name="name", type=str, location="json")
        parser.add_argument(name="url", type=str, location="json")
        parser.add_argument(name="description", type=str, location="json")
        parser.add_argument(name="old_price", type=float, location="json")
        parser.add_argument(name="new_price", type=float, location="json")
        parser.add_argument(name="is_favorite", type=bool, location="json")

        body = parser.parse_args()
        name = body.name
        url = body.url
        description = body.description
        is_favorite = body.is_favorite
        try:
            old_price = float(body.old_price)
            new_price = float(body.new_price)
        except:
            return {"message": "post cái lol gì? giá là số ok? bỏ chữ Đ hay VND đi"}, 401

        discount_rate = 1-new_price/old_price

        if name is None or description is None or url is None or new_price is None or old_price is None or is_favorite is None:
            return {"message": "Gửi cc thiếu trường đcm"}, 401

        rage = Rage.objects().with_id(id)
        rage.update(name = name, url = url, description = description, old_price = old_price, new_price = new_price, discount_rate = discount_rate
                    ,is_favorite = is_favorite)
        update_rage = Rage.objects().with_id(id)
        return mlab.item2json(update_rage),200







