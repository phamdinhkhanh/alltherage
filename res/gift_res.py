from mongoengine import Document, StringField
from flask_restful import Resource, reqparse
from flask import request
import mlab
from model.gift import *


class GiftRes(Resource):
    def post(self):
        # header=request.headers['Dm-Team']
        # if str(header)!="abcxyz":
        #     return {"message":"header đâu đm"},401

        parser = reqparse.RequestParser()
        parser.add_argument(name="code", type=str, location="json")
        parser.add_argument(name="user_number", type=int, location="json")
        parser.add_argument(name="spend_min", type=float, location="json")
        parser.add_argument(name="price", type=float, location="json")

        body=parser.parse_args()
        code=body["code"]
        code=str(code).lower()
        user_number=body["user_number"]
        spend_min=body["spend_min"]
        price=body["price"]
        gifts=GiftCode.objects(code=code)
        for gift in gifts:
            gift.delete()

        gift=GiftCode(code=code,user_number=user_number,spend_min=spend_min,price=price)
        gift.save()
        add_gift=GiftCode.objects().with_id(gift.id)
        return add_gift.to_json()

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="code", type=str, location="json")
        parser.add_argument(name="spend", type=float, location="json")
        body=parser.parse_args()
        code=body["code"]
        code=str(code).lower()
        spend=body["spend"]
        gift=GiftCode.objects(code=code).first()
        if(gift is None):
            return {"message":"code đéo tồn tại ok?"},400
        price=gift.price
        spend_min=gift.spend_min
        if float(spend_min)>float(spend):
            return {"message":"mua thêm mới được e ây, tiền ít có cc"},401

        return {"message":"OK",
                "price":price},200

    def get(self):
        giftcodes = GiftCode.objects()
        return [giftcode.to_json() for giftcode in giftcodes], 200





