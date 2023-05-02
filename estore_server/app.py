from flask import Flask,request,jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from joblib import Parallel, delayed
import joblib
import datetime

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

def get_label(total_purchase, user_importance, total_days, frquency_of_purchases, total_profit):
    labels = ["High", "Low", "Medimum"]
    data = list()
    data.append(list())
    data[0].append(total_purchase)
    data[0].append(user_importance)
    data[0].append(total_days)
    data[0].append(frquency_of_purchases)
    data[0].append(total_profit)
    # Load the model from the file
    model = joblib.load('model.pkl')
    # Use the loaded model to make predictions
    result = model.predict(data)
    return labels[result[0]]

@app.route('/login',methods=['GET'])
def login():
    args = request.args
    email = args.get("email")
    
    df = pd.read_csv('customer.csv')
    row = df.loc[df['email']==email]
    if(len(row)>0):
        userId=row['id'].values[0]
        return jsonify({"success":1,"userId":userId})
    
    return jsonify({"succes":0})



@app.route('/discount',methods=['GET'])
def getDiscount():
    # total_purchase = 50
    # user_importance = 0.9
    # total_days = 400
    # frquency_of_purchases = 0.1
    # total_profit = 0.1

    # get user id from query params
    args = request.args
    uid = int(args.get("uid"))
    print(uid)
    # uid = 565
    total_profit=0
    df = pd.read_csv('order_data.csv')
    rows = df.loc[df['customer_id']==uid]
    total_purchase = len(rows)
    
    for index,row in rows.iterrows():
        total_profit += float(row['total_profit'])
    
    total_profit = min(1.0,total_profit)

    df = pd.read_csv('customer.csv')
    row = df.loc[df['id']==uid]
    joiningDate = row['date'].values[0]
    unsuccessfulDeals = row['unsuccessful_deals'].values[0]

    date_obj = datetime.datetime.strptime(joiningDate, '%d-%m-%y').date()
    delta = datetime.date.today() - date_obj
    total_days = delta.days

    frquency_of_purchases = min(total_purchase/(total_purchase+unsuccessfulDeals),1.0)
    user_importance=1.0
    if total_purchase>0:
        user_importance = unsuccessfulDeals/(total_purchase+unsuccessfulDeals)

    print(total_purchase,user_importance,total_days,frquency_of_purchases,total_profit)
    discount = {"High":0.3,"Medimum":0.2,"Low":0.1}
    # label = get_label(50, 0.9, 400, 0.1, 0)
    # print(label)
    label = get_label(total_purchase, user_importance, total_days, frquency_of_purchases, total_profit)
    return jsonify({"discount":discount[label]})

@app.route('/data',methods=['POST'])
def postData():
    response = request.get_json()
    print(response)
    return jsonify({"success":1})


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
