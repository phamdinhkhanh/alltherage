from flask_restful import Resource, reqparse
from model.order import *
from model.customer import Customer
from model.rage import Rage
import mlab
from pyfcm.fcm import FCMNotification
import json
import requests
from model.comment import *
import datetime


class CommentRes(Resource):
    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument(name = "user_id", type = str, location = "json")
        parser.add_argument(name = "message", type = str, location = "json")
        body = parser.parse_args()
        id_user = body["user_id"]
        message = body["message"]
        rage = Rage.objects().with_id(id)
        customer = Customer.objects().with_id(id_user)
        date = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
        comment = Comment(customer = customer, message = message, date = str(date),rage = rage)
        comment.save()
        comment_add = Comment.objects().with_id(comment.id)
        return mlab.item2json(comment_add),200

    def get(self,id):
        rage = Rage.objects().with_id(id)
        comments = Comment.objects(rage = rage)
        return mlab.list2json(comments), 200

class CommentIDRes(Resource):
    def get(self,id1,id2):
        comment = Comment.objects().with_id(id2)
        if comment is not None:
            return mlab.item2json(comment),200
        else:
            return {"message":"Lam gi co comment nay"}, 200

    def delete(self,id1,id2):
        comment = Comment.objects().with_id(id2)
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
        comment = Comment.objects().with_id(id2)
        date = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
        comment.update(message = message, date = str(date))
        comment.save()
        comment_add = Comment.objects().with_id(id2)
        return mlab.item2json(comment_add),200