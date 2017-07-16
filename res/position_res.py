from mongoengine import Document, StringField
from flask_restful import Resource, reqparse
import mlab
from model.position import *

class PositionRes(Resource):
    def get(self):
        position = Position.objects()
        return mlab.list2json(position), 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name="name", type=str, location="json")
        parser.add_argument(name="url", type=str, location="json")
        parser.add_argument(name="website", type=str, location="json")
        parser.add_argument(name="address", type=str, location="json")
        parser.add_argument(name="description", type=str, location="json")
        parser.add_argument(name="opentime", type=str, location="json")
        parser.add_argument(name="phone", type=str, location="json")
        parser.add_argument(name="longtitude", type=str, location="json")
        parser.add_argument(name="latitude", type=str, location="json")
        parser.add_argument(name="number_seen", type=int, location="json")
        parser.add_argument(name="code", type=str, location="json")
        parser.add_argument(name="user_id", type=str, location="json")

        body = parser.parse_args()
        name = body.name
        url = body.url
        website = body.website
        address = body.address
        description = body.description
        opentime = body.opentime
        phone = body.phone
        longtitude = body.longtitude
        latitude = body.latitude,
        number_seen = body.number_seen,
        code = body.code
        user_id = body.user_id

        if name is None or address is None or longtitude is None or latitude is None \
                or code is None or user_id is None:
            return {"message": "Gửi cc thiếu trường đcm"}, 401
        found_position = Position.objects(longtitude = longtitude, latitude = latitude)
        # if found_position is not None:
        #      return {"message":"Position already exist"}, 401
        print(123)
        position = Position(name=name, url=url, website=website, address = address,description = description,
                            opentime = opentime, phone = phone, latitude = latitude,longtitude = longtitude)\
            # ,
            #                 code = code, user_id = Customer.objects().with_id(user_id))
        position.save()

        add_position = Position.objects().with_id(position.id)
        return mlab.item2json(add_position), 200

class PositionNumberSeenUpdate(Resource):
    def put(self,id):
        position = Position.objects().with_id(id)
        current_number_seen = position.number_seen
        if current_number_seen is None:
            number_seen = 1
        else: number_seen = current_number_seen + 1
        position.update(number_seen = number_seen)
        update_position = Position.objects().with_id(position.id)
        return mlab.item2json(update_position)

class APositionRes(Resource):
    def get(self,id):
        position = Position.objects().with_id(id)
        return mlab.item2json(position), 200

    def delete(self,id):
        position = Position.objects().with_id(id)
        position.delete()
        return {"message":"OK"},200


    def put(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument(name="name", type=str, location="json")
        parser.add_argument(name="url", type=str, location="json")
        parser.add_argument(name="website", type=str, location="json")
        parser.add_argument(name="address", type=str, location="json")
        parser.add_argument(name="description", type=str, location="json")
        parser.add_argument(name="opentime", type=str, location="json")
        parser.add_argument(name="phone", type=str, location="json")
        parser.add_argument(name="longtitude", type=float, location="json")
        parser.add_argument(name="latitude", type=float, location="json")
        parser.add_argument(name="number_seen", type=int, location="json")
        parser.add_argument(name="code", type=str, location="json")
        parser.add_argument(name="user_id", type=str, location="json")

        body = parser.parse_args()
        name = body.name
        url = body.url
        website = body.website
        address = body.address
        description = body.description
        opentime = body.opentime
        phone = body.phone
        longtitude = body.longtitude
        latitude = body.latitude,
        number_seen = body.number_seen,
        user_id = body.user_id,
        code = body.code

        try:
            longtitude = float(body.longtitude)
            latitude = float(body.latitude)
        except:
            return {"message": "longtitude,latitude là số"}, 401

        if name is None or address is None or description is None or longtitude is None or latitude is None or code is None or user_id is None:
            return {"message": "Gửi cc thiếu trường đcm"}, 401

        position = Position.objects().with_id(id)
        position.update(name=name, url=url,website=website ,address = address,description = description, opentime = opentime , phone = phone,longtitude = longtitude,latitude = latitude,
                            number_seen = None, code = code, user_id = Customer.objects.with_id(user_id))
        update_position = Position.objects().with_id(id)
        return mlab.item2json(update_position),200






