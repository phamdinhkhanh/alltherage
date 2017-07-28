from flask import Flask
import mlab
from flask_restful import Resource, Api

from res.comment_res import *
from res.commentposition_res import CommentPositionRes, CommentPositionUpdate, CommentPositionIDRes
from res.rage_res import *
from res.user_res import *
from res.order_res import *
from res.gift_res import *
from res.login import jwt_init,RegisterRes
from res.position_res import *
import logging
import sys

mlab.connect()

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
api = Api(app)
jwt = jwt_init(app)



api.add_resource(RageRes,"/api/rage")
api.add_resource(ARageRes,"/api/rage/<id>")
#update number_seen into rage
api.add_resource(RageUpdate,"/api/rage/seen/<id>")
#comment into rage
api.add_resource(CommentRes,"/api/rage/comment/<id>")
#comment update
api.add_resource(CommentUpdate,"/api/comment/<id>")
#get a comment detail
api.add_resource(CommentIDRes,"/api/rage/comment/<id1>/<id2>")
#get customer by id in mlab
api.add_resource(ACustomer,"/api/register/<id>")
#update customer order address
api.add_resource(UpdateAddressOrder,"/api/register/updateAddressOrder/<id>")
#update customer facebook
api.add_resource(UpdateFb,"/api/register/updateFb/<id>")
#update customer google
api.add_resource(UpdateGG,"/api/register/updateGG/<id>")
#update customer facebook
api.add_resource(UpdatePhone,"/api/register/updatePhone/<id>")
#update mamay
api.add_resource(UpdateMamay,"/api/register/updateMamay/<id>")
#get customer by username
api.add_resource(ACustomerByName,"/api/username/<id>")
#get customer order
api.add_resource(OrderCustomer,"/api/register/order/<id>")
#get customer order last
api.add_resource(OrderLastCustomer,"/api/register/orderlast/<id>")
#delete customer
api.add_resource(RegisterRes,"/api/register")
#get list rage customer like
api.add_resource(CustomerRageLike,"/register/like/<id>")
#post a new order list
api.add_resource(OrderRes,"/order")
#get spend ship
api.add_resource(OrderShipSpend,"/orderShipSpend")
#add into customer total spend when order success
api.add_resource(OrderTotalSpend,"/order/<id>")
#add gift code
api.add_resource(GiftRes,"/giftcode")
#get all position
api.add_resource(PositionRes,"/api/position")
#put a postion
api.add_resource(APositionRes,"/api/position/<id>")
#update number seen
api.add_resource(PositionNumberSeenUpdate,"/api/posititon/numberseen/<id>")
#update number like
api.add_resource(PositionNumberLikeUpdate,"/api/posititon/numberlike/<id>")
#position number rating
api.add_resource(PositionRating,"/api/posititon/rating/<id>")
#position rating value
api.add_resource(PositionRatingRes,"/api/posititon/ratingvalue/<id>")
#comment into position
api.add_resource(CommentPositionRes,"/api/position/comment/<id>")
#comment update in position
api.add_resource(CommentPositionUpdate,"/api/commentposition/<id>")
#get a comment detail in position
api.add_resource(CommentPositionIDRes,"/api/position/comment/<id1>/<id2>")

@app.route('/')
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run()
