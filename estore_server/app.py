from flask import Flask,request,jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.sqlite3'
db = SQLAlchemy(app)

class OrderItems(db.Model):
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   order_id = db.Column(db.String(200))
   user_id = db.Column(db.String(200))
   product = db.Column(db.String(50))
   price = db.Column(db.Integer)
   quantity = db.Column(db.Integer)

   def __init__(self, order_id, user_id, product, price, quantity):
        self.user_id = user_id
        self.product = product
        self.price = price
        self.quantity = quantity
        self.order_id = order_id
   

CORS(app)

@app.route('/postOrder',methods=['POST'])
def postOrder():
    
    response =  request.get_json()
    # create random user id 
    user_id = str(uuid.uuid1())
    # create order id
    order_id = str(uuid.uuid1())
    products = response['data']
    for product in products:
        order = OrderItems(order_id,user_id,product[0],product[1],product[2])
        db.session.add(order)
        db.session.commit()
    # postOrder(response['text'])
    items = db.session.query(OrderItems).all()
    for item in items:
        print(item.order_id,item.user_id,item.product,item.price,item.quantity)

    return jsonify({"success":1})
    
@app.route('/products')
def getProducts():
    

    return jsonify({
            "tomatoes":{"price":500,"qty":400},
            "potatoes":{"price":400,"qty":300},
            "apples":{"price":300,"qty":100},
            "banannas":{"price":100,"qty":200},
            "grapes":{"price":100,"qty":200},
            "onions":{"price":200,"qty":100},
            "chicken":{"price":200,"qty":100},
            "butter":{"price":200,"qty":100},
            "yogurt":{"price":400,"qty":100},
            "brown bread":{"price":300,"qty":100},
            "flour":{"price":200,"qty":100},
            "sugar":{"price":200,"qty":100},
            "coffee":{"price":200,"qty":100},
            "beef":{"price":300,"qty":100},
            "beries":{"price":200,"qty":100},
            "fish":{"price":200,"qty":100},
            "pasta":{"price":200,"qty":100},
            "sausage":{"price":100,"qty":100},
            "dessert":{"price":200,"qty":100},
            "cream cheese":{"price":200,"qty":100},
            "eggs":{"price":200,"qty":100},
            "salt":{"price":400,"qty":100},
            "oil":{"price":200,"qty":100},
            "water":{"price":200,"qty":100},
            "coffee":{"price":200,"qty":100},
            "cabbage":{"price":300,"qty":100},
            "mushroom":{"price":200,"qty":100},
            "broccoli":{"price":700,"qty":100},
            "peas":{"price":800,"qty":100}
        })


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
