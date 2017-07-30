from flask_restful import Resource, reqparse

from model.commentposition import CommentPostion
from model.order import *
from model.customer import Customer
from model.position import Position
from model.rage import Rage
import mlab
from pyfcm.fcm import FCMNotification
import json
import requests
from model.comment import *
from res.position_res import *
import datetime


class CommentPositionRes(Resource):
    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument(name = "user_id", type = str, location = "json")
        parser.add_argument(name = "message", type = str, location = "json")
        parser.add_argument(name = "rating", type = int, location = "json")
        body = parser.parse_args()
        id_user = body["user_id"]
        message = body["message"]
        rating = body["rating"]
        position = Position.objects().with_id(id)
        customer = Customer.objects().with_id(id_user)
        date = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
        comment = CommentPostion(customer = customer, message = message, date = str(date),position = position, rating = rating)
        #update position rating
        if rating is None:
            comment.save()
            comment_add = CommentPostion.objects().with_id(comment.id)
            return comment_add.get_json(), 200
        if rating > 5 or rating < 1:
            return {"message":"Rating sai giá trị"}, 401
        position = Position.objects().with_id(id)
        if position is None:
            return {"message": "Không tồn tại"}, 401
        if position.rating is None:
            current_rating = 0
        else:
            current_rating = position.rating
        if position.number_rating is None:
            current_number_rating = 0
        else:
            current_number_rating = position.number_rating
        update_rating = (current_rating*current_number_rating+rating)/(current_number_rating+1)
        position.update(number_rating=current_number_rating+1,rating = update_rating)
        comment.save()
        comment_add = CommentPostion.objects().with_id(comment.id)
        return comment_add.get_json(),200

    def get(self,id):
        position = Position.objects().with_id(id)
        comments = CommentPostion.objects(position = position)
        l = [item.get_json() for item in comments]
        # l = mlab.list2json(comments)
        return l,200

    def delete(self,id):
        position = Position.objects().with_id(id)
        comments = CommentPostion.objects(position=position)
        l = [item.get_json() for item in comments]
        for cm in comments:
            cm.delete()
        return {"message": "OK"}, 200


class CommentPositionUpdate(Resource):
    def get(self,id):
        comment = CommentPostion.objects().with_id(id)
        return comment.get_json(),200

    def put(self,id):
        parser = reqparse.RequestParser()
        parser.add_argument(name="numberlike", type=int, location="json")
        body = parser.parse_args()
        numberlike = body["numberlike"]
        comment = CommentPostion.objects().with_id(id)
        comment.update(numberlike = numberlike)
        updatecomment = CommentPostion.objects().with_id(id)
        return updatecomment.get_json()

class CommentPositionIDRes(Resource):
    def get(self,id1,id2):
        comment = CommentPostion.objects().with_id(id2)
        if comment is not None:
            return mlab.item2json(comment),200
        else:
            return {"message":"Lam gi co comment nay"}, 200

    def delete(self,id1,id2):
        comment = CommentPostion.objects().with_id(id2)
        if comment is not None:
            comment.delete()
            return {"message":"OK"},200
        else:
            return {"message":"Lam gi co comment nay"}, 200

    def put(self,id1,id2):
        parser = reqparse.RequestParser()
        parser.add_argument(name="message", type=str, location="json")
        body = parser.parse_args()
        message = body["message"]
        comment = CommentPostion.objects().with_id(id2)
        date = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
        comment.update(message = message, date = str(date))
        comment.save()
        comment_add = CommentPostion.objects().with_id(id2)
        return mlab.item2json(comment_add),200


