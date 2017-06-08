from flask_restful import Resource, reqparse
from model.order import *
from model.customer import Customer
from model.rage import Rage
import mlab
from pyfcm.fcm import FCMNotification
import json
import requests
import datetime
from model.gift import *

class OrderRes(Resource):
    def get(self):
        orders = Order.objects(is_Success = False)
        return mlab.list2json(orders)
        #return [order.get_json() for order in orders], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="items", type = list, location = "json")
        parser.add_argument(name="address_order", type=str, location="json")
        parser.add_argument(name="phone_number", type=str, location="json")
        parser.add_argument(name="user_id", type=str, location="json")
        parser.add_argument(name="code", type=str, location="json")
        body = parser.parse_args()
        items = body["items"]
        date = datetime.datetime.today().strftime('%d-%m-%Y')
        address_order = body.address_order
        phone_number = body.phone_number
        user_id = body.user_id
        code = body["code"]

        if items is None or date is None or address_order is None or phone_number is None or user_id is None or code is None:
            return {"message":"Thiếu trường rồi mày"}, 401

        if len(str(phone_number)) < 10 or len(str(phone_number)) > 11:
            return {"messsage":"Đây mà là số điện thoại, mày điên ah? 10 hoặc 11 số nhé c hó"}, 401

        try:
            sdt = float(phone_number)
        except:
            return {"message":"Điện thoại cứt gì mà có chữ"},401

        #API_KEY = "AIzaSyDngB6pcJy3bHN4GuWZCaJGrb3sQUxWtCo"
        API_KEY = "AIzaSyCEB4QVng3uFEQ-SwxfwOWAG4H3sr7Mfi8"
        url_request = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=vi-VN&key={2}".format(
            "số nhà 1A/178, đường Hoàng Mai , quận Hoàng Mai, thành phố Hà nội", str(address_order) + " Hà Nội", API_KEY)

        ship_spend = 0
        try:
            req = requests.get(url_request)
            json_data = json.loads(req.content)
            list_add = json_data["rows"]
            elements = list_add[0]["elements"]
            km = elements[0]["distance"]["text"]
            txt = str(km).split(" ")
            distance = txt[0].replace(",",".")
            ship_spend = float(distance)*3000
        except:
            ship_spend = -1
        order_items = []
        spend = 0
        for item in items:
            rage_id = item["id"]
            count = item["count"]
            try:
                sl = int(count)
                if sl < 1:
                    return {"message":"Số lượng > 0 hả mày?"},401
            except:
                return {"message":"count là int ok mày?"}, 401
            rage = Rage.objects().with_id(rage_id)
            single_order = SingleOrder(count=count, rage=rage)
            order_items.append(single_order)
            spend += float(rage["new_price"])*sl
        if spend == 0:
            return {"message":"đặt hàng cc gì mà bằng 0"}, 401
        try:
            customer = Customer.objects().with_id(user_id)
            customer.update(address_order = address_order,phone_number = phone_number)
        except:
            return {"message":"userid của mày bị điên ah"},401

        code = str(code).lower()
        gift = GiftCode.objects().filter(code=code)
        code_price = gift[0]["price"]
        try:
            spend_min = gift[0]["spend_min"]
        except:
            spend_min = -1
        if (spend > 0 and (spend >= spend_min and spend_min != -1)):
            user_number = gift[0]["user_number"]
            user_number -= 1
            if user_number == 0:
                gift[0].delete()
            else:
                gift[0].update(user_number = user_number)
            # print("order_items")
            # print(order_items)
            # print("date")
            # print(date)
            # print("address_order")
            # print(address_order)
            # print("phone_number")
            # print(phone_number)
            # print("user")
            # print(Customer.objects().with_id(user_id).get_json())
            # print("spend")
            # print(spend + ship_spend - code_price)
            # print("ship_money")
            # print(ship_spend)
            # print("code")
            # print(code)
            # print("code_price")
            # print(code_price)


            order = Order(items = order_items, date = date, address_order = address_order, phone_number = phone_number,
                          customer = Customer.objects().with_id(user_id),is_Success = False,
                          spend = spend + ship_spend - code_price, ship_money = ship_spend,code = code,
                          code_price = code_price)
        else:
            order = Order(items = order_items, date = date, address_order = address_order, phone_number = phone_number,
                          customer = Customer.objects().with_id(user_id),is_Success = False,code = code,
                          spend = spend + ship_spend, ship_money = ship_spend,
                          code_price = code_price)
        order.save()
        add_order = Order.objects().with_id(order.id)
        apikey = "blablalaa"
        #push_service = FCMNotification(api_key=apikey)
        #push_service.notify_topic_subscribers(topic_name="admin", message_body="Có đơn hàng mới",
        #                                      message_title="Kiểm tra ngay")
        return mlab.item2json(add_order), 200

class OrderTotalSpend(Resource):
    def get(self,id):
        order = Order.objects().with_id(id)
        return mlab.item2json(order)

    def put(self, id):
        order = Order.objects().with_id(id)
        if order.is_Success != True:
            order.update(set__is_Success = True)
            order_add = Order.objects().with_id(id)
            customer = order["customer"]
            spend = float(order["spend"])
            if customer["total_spend"] is not None:
                spend_user = float(customer["total_spend"])
                total = spend + spend_user
            else:
                total = spend
            customer.update(total_spend = total)
            return mlab.item2json(customer), 200
        else:
            return {"message":"đơn hàng đã success rồi còn push lại làm gì?"},200

    def delete(self, id):
        order = Order.objects().with_id(id)
        order.delete()
        return {"message":"OK"},200

class OrderCustomer(Resource):
    def get(self,id):
        customer = Customer.objects().with_id(id)
        order = Order.objects(Customer == customer)
        return mlab.item2json(order)












