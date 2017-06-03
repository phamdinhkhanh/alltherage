from flask import Flask
import mlab
from flask_restful import Resource, Api

from res.comment_res import *
from res.rage_res import *
from res.user_res import *
from res.order_res import *
from res.gift_res import *
from res.login import jwt_init,RegisterRes


mlab.connect()

app = Flask(__name__)
api = Api(app)
jwt = jwt_init(app)



api.add_resource(RageRes,"/api/rage")
api.add_resource(ARageRes,"/api/rage/<id>")
#comment into rage
api.add_resource(CommentRes,"/api/rage/comment/<id>")
#get a comment detail
api.add_resource(CommentIDRes,"/api/rage/comment/<id1>/<id2>")
#get customer
api.add_resource(ACustomer,"/api/register/<id>")
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

#api.add_resource(User,"/api/user/<id>")
#api.add_resource(UserRegister,"/user")
#api.add_resource(UserUpdate,"/user/<id>")
#api.add_resource(OderRes, "/oder")
#api.add_resource(OderSuccus,"/oder/<id>")
#api.add_resource(FoodRate,"/rate/<id>")
#api.add_resource(FoodGetHotSales,"/food/hot")
#api.add_resource(FoodFavorite,"/food/favorite")
#api.add_resource(UserFoodLike,"/food/like/<id>")
#api.add_resource(OrderAdmin,"/oder/success")
#api.add_resource(UserOrderVerify,"/oder/<id>/verify")
#api.add_resource(UserOrderSuccess,"/oder/<id>/success")
#api.add_resource(TotalMoneyDay,"/oder/moneyday")
#api.add_resource(TotalMoneyMonth,"/oder/moneymonth")
#api.add_resource(TotalMoneyYear,"/oder/moneyyear")
#api.add_resource(TotalMoney,"/oder/money")
#api.add_resource(PushNotification,"/notification")
#api.add_resource(FoodLike,"/food/islike/<id>")
#api.add_resource(CommentRes,"/comment/<id>")
#api.add_resource(UserSpend,"/oder/totalspend/<id>")
#api.add_resource(FoodInfoRes,"/food/info")
#api.add_resource(FoodInfoGetRes,"/food/info/<id>")
#api.add_resource(GetCover,"/cv")
#api.add_resource(GiftRes,"/giftcode")


@app.route('/')
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run()
