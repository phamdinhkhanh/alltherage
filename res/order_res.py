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
import re
class OrderRes(Resource):
    def get(self):
        orders = Order.objects(is_Success = False)
        return mlab.list2json(orders)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="items", action = "append", location = "json")
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
        print("item:",items);
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
            #Làm tròn tiền ship chia hết cho 5
            ship_spend = round(round(float(distance)*3000,0)/5000,0)*5000
            if(ship_spend > 50000):
                ship_spend = 50000
            print("ship_spend:",ship_spend,"address:",json_data)
        except:
            ship_spend = -1
            return {"message":"Địa chỉ không hợp lệ!"}, 401
        order_items = []
        spend = 0
        #Tạo dumps string
        dumps = json.dumps(items)
        #List dumps
        ldumps = re.findall(r"[\w']+",dumps)
        print("ldumps:",ldumps)
        print("rage_id",ldumps[1][1:-1])
        print("count",ldumps[3])
        for i in range(0,len(items)+1):
            try:
                rage_id = ldumps[4*i+1][1:-1]
                count = int(ldumps[4*i+3])
                rage = Rage.objects().with_id(rage_id)
                single_order = SingleOrder(count=count, rage=rage)
                price = rage.new_price
                sl = int(count)
                try:
                    if sl < 1:
                        return {"message":"Số lượng phải > 0"},401
                except:
                    return {"message":"count là int ok mày?"},401
                order_items.append(single_order)
                spend += (price * sl)
            except: print("Index error")
        if spend == 0:
            return {"message":"đặt hàng cc gì mà bằng 0"}, 401
        try:
            customer = Customer.objects().with_id(user_id)
            customer.update(address_order = address_order,phone_number = phone_number)
        except:
            return {"message":"userid của mày bị điên ah"},401

        code = str(code).lower()
        gift = GiftCode.objects(code = code).first()
        print("get Codeprice")
        code_price = gift.price
        try:
            spend_min = gift.spend_min
        except:
            spend_min = -1
        if (spend > 0 and (spend >= spend_min and spend_min != -1)):
            user_number = gift["user_number"]
            user_number -= 1
            if user_number == 0:
                gift.delete()
            else:
                gift.update(user_number=user_number)
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

class OrderShipSpend(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="address_order", action="str", location="json")
        body = parser.parse_args()
        address_order = body["address_order"]
        API_KEY = "AIzaSyCEB4QVng3uFEQ-SwxfwOWAG4H3sr7Mfi8"
        url_request = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=driving&language=vi-VN&key={2}".format(
            "số nhà 1A/178, đường Hoàng Mai , quận Hoàng Mai, thành phố Hà nội", str(address_order) + " Hà Nội",
            API_KEY)
        try:
            req = requests.get(url_request)
            json_data = json.loads(req.content)
            list_add = json_data["rows"]
            elements = list_add[0]["elements"]
            km = elements[0]["distance"]["text"]
            txt = str(km).split(" ")
            distance = txt[0].replace(",", ".")
            # Làm tròn tiền ship chia hết cho 5
            print("distance:",distance)
            ship_spend = round(round(float(distance)*3000,0)/5000,0)*5000
            if(ship_spend > 50000):
                ship_spend = 50000
            print("ship_spend:", ship_spend, "address:", json_data)
            return {"ship_spend":ship_spend}, 200
        except:
            ship_spend = -1
            return {"message": "Địa chỉ không hợp lệ!"}, 401


class OrderTotalSpend(Resource):
    def get(self,id):
        order = Order.objects().with_id(id)
        return mlab.item2json(order)

    def put(self, id):
        order = Order.objects().with_id(id)
        if order.is_Success != True:
            order.update(set__is_Success = True)
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

class OrderLastCustomer(Resource):
    def get(self,id):
        customer = Customer.objects().with_id(id)
        order = Order.objects(Customer == customer).order_by('-id')[0]
        order.get_singleOrders();
        return order.get_singleOrders();

class OrderCustomer(Resource):
    def get(self,id):
        customer = Customer.objects().with_id(id)
        order = Order.objects(Customer == customer)
        return mlab.item2json(order)


    def delete(self,id):
        customer = Customer.objects().with_id(id)
        order = Order.objects(Customer == customer)
        order.delete()
        return {"message":"OK"},200










