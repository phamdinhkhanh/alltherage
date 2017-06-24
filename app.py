from flask import Flask
import mlab
from flask_restful import Resource, Api

from res.comment_res import *
from res.rage_res import *
from res.user_res import *
from res.order_res import *
from res.gift_res import *
from res.login import jwt_init,RegisterRes
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
#comment into rage
api.add_resource(CommentRes,"/api/rage/comment/<id>")
#get a comment detail
api.add_resource(CommentIDRes,"/api/rage/comment/<id1>/<id2>")
#get customer by id in mlab
api.add_resource(ACustomer,"/api/register/<id>")
#update customer order address
api.add_resource(UpdateAddressOrder,"/api/register/updateAddressOrder/<id>")
#get customer by username
api.add_resource(ACustomerByName,"/api/username/<id>")
#get customer order
api.add_resource(OrderCustomer,"/api/register/order/<id>")
#delete customer
api.add_resource(RegisterRes,"/api/register")
#get list rage customer like
api.add_resource(CustomerRageLike,"/register/like/<id>")
#post a new order list
api.add_resource(OrderRes,"/order")
#add into customer total spend when order success
api.add_resource(OrderTotalSpend,"/order/<id>")
#add gift code
api.add_resource(GiftRes,"/giftcode")

@app.route('/')
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run()
