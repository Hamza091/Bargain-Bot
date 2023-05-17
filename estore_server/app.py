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
import random
import datetime
import csv

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.sqlite3'
db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.String(200),primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    date = db.Column(db.String(200))
    unsuccessful_deals = db.Column(db.String(200))

    def __init__(self,id,first_name,last_name,email,date,unsuccessful_deals):
        self.id = id
        self.first_name=first_name
        self.last_name=last_name
        self.email=email
        self.date=date
        self.unsuccessful_deals=unsuccessful_deals


class OrderItems(db.Model):
    order_id = db.Column(db.String(200),primary_key=True)
    customer_id = db.Column(db.String(200))
    date_of_order = db.Column(db.String(200))
    total_profit = db.Column(db.Integer)
    selling_price = db.Column(db.Integer)


    def __init__(self, order_id, user_id, price, date_of_order, total_profit):
        self.customer_id = user_id
        self.total_profit = total_profit
        self.date_of_order = date_of_order
        # self.product = product
        self.selling_price = price
        # self.quantity = quantity
        self.order_id = order_id
   

class Products(db.Model):
    id = db.Column(db.String(200),primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    maxDiscount = db.Column(db.Float)

    def __init__(self,id,name,price,qty,maxDiscount):
        self.id = id
        self.name = name
        self.price = price
        self.qty = qty
        self.maxDiscount = maxDiscount

CORS(app)

def import_csv_to_database(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['id']=='': 
                break
            my_model_instance = Customer(
                id = row['id'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                date =row['date'],
                unsuccessful_deals = row['unsuccessful_deals']
            )
            db.session.add(my_model_instance)
        db.session.commit()

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

enableCounterOffer = None
@app.route('/negoMode',methods=['GET'])
def negoMode():
    return jsonify({"enableCounterOffer":enableCounterOffer})

@app.route('/login',methods=['POST'])
def login():
    global enableCounterOffer
    data = request.get_json() 
    print(request.get_json())
    email = data["email"]
    enableCounterOffer = data["enableCounterOffer"]
    customer = db.session.query(Customer).filter_by(email=email).all()
    
    if(len(customer)>0):
        return jsonify({"success":1,"userId":int(customer[0].id)})
    
    return jsonify({"success":0})



@app.route('/discount',methods=['GET'])
def getDiscount():
    # total_purchase = 50
    # user_importance = 0.9
    # total_days = 400
    # frquency_of_purchases = 0.1
    # total_profit = 0.1
    args = request.args
    
    uid = args.get("uid")
    # print(uid)
    # uid = 565
    total_profit=0
    rows= db.session.query(OrderItems).filter_by(customer_id=uid).all()
    total_purchase = len(rows)

    for row in rows:
        total_profit += float(row.total_profit)
    
    total_profit = min(1.0,total_profit)

    # row = db.session.query(Customer).filter_by(id)
    # print(row)
    row = Customer.query.get(uid)
    joiningDate = row.date
    unsuccessfulDeals = int(row.unsuccessful_deals)

    date_obj = datetime.datetime.strptime(joiningDate, '%d-%m-%y').date()
    delta = datetime.date.today() - date_obj
    total_days = delta.days

    frquency_of_purchases = min(total_purchase/(total_purchase+unsuccessfulDeals),1.0)
    user_importance=1.0
    if total_purchase>0:
        user_importance = unsuccessfulDeals/(total_purchase+unsuccessfulDeals)

    # print(total_purchase,user_importance,total_days,frquency_of_purchases,total_profit)
    # discount = {"High":0.3,"Medimum":0.2,"Low":0.1}
    label = get_label(50, 0.9, 400, 0.1, 0)
    # # print(label)
    label = get_label(total_purchase, user_importance, total_days, frquency_of_purchases, total_profit)
    return jsonify({"discount":label[0]})
    # return jsonify({"no":"no"})

@app.route('/data',methods=['POST'])
def postData():
    response = request.get_json()
    print(response)
    return jsonify({"success":1})


@app.route('/postOrder',methods=['POST'])
def postOrder():
    
    response =  request.get_json()
    order_id = str(uuid.uuid1())
    products = response['data']
    customer_id = response['userId']
    date_of_order = str(datetime.date.today())
    netDiscountReceived = response['netDiscountReceived']
    total_price = 0
    for product in products:
        total_price += int(product[1])
    selling_price = total_price-netDiscountReceived
    total_profit = round(random.uniform(0,0.8),2)


    order = OrderItems(order_id,customer_id,selling_price,date_of_order,total_profit)
    db.session.add(order)
    db.session.commit()
    print(order)

    return jsonify({"success":1})
    
@app.route('/products')
def getProducts():
    
    products = {}
    rows  = db.session.query(Products).all()
    for row in rows:
        products[row.name] = {"price":row.price,"qty":row.qty,"maxDiscount":row.maxDiscount}
    # print(products)
    return jsonify(products)
    # return jsonify({
    #         "tomatoes":{"price":95,"qty":400,"maxDiscount":0.28},
    #         "potatoes":{"price":90,"qty":300,"maxDiscount":0.15},
    #         "apples":{"price":300,"qty":100,"maxDiscount":0.27},
    #         "banannas":{"price":400,"qty":200,"maxDiscount":0.13},
    #         "grapes":{"price":100,"qty":200,"maxDiscount":0.14},
    #         "onions":{"price":90,"qty":100,"maxDiscount":0.29},
    #         "chicken":{"price":200,"qty":100,"maxDiscount":0.29},
    #         "butter":{"price":200,"qty":100,"maxDiscount":0.3},
    #         "yogurt":{"price":400,"qty":100,"maxDiscount":0.2},
    #         "brown bread":{"price":300,"qty":100,"maxDiscount":0.2},
    #         "flour":{"price":200,"qty":100,"maxDiscount":0.2},
    #         "sugar":{"price":135,"qty":100,"maxDiscount":0.2},
    #         "coffee":{"price":200,"qty":100,"maxDiscount":0.2},
    #         "beef":{"price":300,"qty":100,"maxDiscount":0.2},
    #         "beries":{"price":200,"qty":100,"maxDiscount":0.5},
    #         "fish":{"price":200,"qty":100,"maxDiscount":0.2},
    #         "pasta":{"price":200,"qty":100,"maxDiscount":0.2},
    #         "sausage":{"price":100,"qty":100,"maxDiscount":0.2},
    #         "dessert":{"price":200,"qty":100,"maxDiscount":0.5},
    #         "cream cheese":{"price":200,"qty":100,"maxDiscount":0.2},
    #         "eggs":{"price":200,"qty":100,"maxDiscount":0.2},
    #         "salt":{"price":400,"qty":100,"maxDiscount":0.4},
    #         "oil":{"price":200,"qty":100,"maxDiscount":0.2},
    #         "water":{"price":200,"qty":100,"maxDiscount":0.2},
    #         "coffee":{"price":200,"qty":100,"maxDiscount":0.2},
    #         "cabbage":{"price":300,"qty":100,"maxDiscount":0.2},
    #         "mushroom":{"price":200,"qty":100,"maxDiscount":0.2},
    #         "broccoli":{"price":700,"qty":100,"maxDiscount":0.2},
    #         "peas":{"price":800,"qty":100,"maxDiscount":0.2}
    #     })


if __name__ == '__main__':
    # with app.app_context():
    #     items = db.session.query(Products).all()
    #     for item in items:
    #         # print(item.id,item.name,item.qty,item.price,item.maxDiscount)
    #         item.maxDiscount = round(random.uniform(0.1,0.3),2)
    #         db.session.commit()
    #     # db.create_all()
    #     items = db.session.query(Products).all()
    #     for item in items:
    #         print(item.id,item.name,item.qty,item.price,item.maxDiscount)

        
        # items = db.session.query(Customer).all()
        # for item in items:
        #     print(item.id,item.first_name,item.last_name)
        # print(items)
        # import_csv_to_database('customer.csv')
    app.run()
