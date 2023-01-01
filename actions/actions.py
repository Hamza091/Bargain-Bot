# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re
import requests
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionProductQuery(Action):

    def name(self) -> Text:
        return "action_product_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:       
        
        # extract all product names and their quantities
        products = []
        entities = tracker.latest_message['entities']
        
        quantity="1"
        product=""
        for entity in entities:    
            if entity['entity']=='quantity':
                quantity = entity['value']
            elif entity['entity']=='product':
                product = entity['value']
                # if product is found then it is expected that quantity is also found for that product if not then it's default valud would be 1
                #convert quantity to int and remove the unit 
                #removing non-digit characters using regex
                qty = re.sub(r"\D","",quantity)
                
                products.append([product,int(qty)])
                quantity="1"
        
        #print(products)
        # check if products are available
        
        estoreProducts = {
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
        }

        available = []
        unavailable = []

        for product in products:
            name = product[0]
            qty = product[1]
            if name in estoreProducts and estoreProducts[name]["qty"]>=qty:
                    # product is available with required quantity
                    # calculate total price and append in available array
                    totalPrice = estoreProducts[name]["price"]*qty
                    available.append([name,totalPrice,qty])
            else:
                # product is not available
                unavailable.append(name)

        #generate response
        # print(available)
        # print(unavailable)
        #response for available product
        response=""
        

        if len(available)>0:
            
            for product in available:
                response+=product[0]
                if(product!=available[len(available)-1]):
                    response+=","
            
            if len(available)>1:
                response+=" are available. "
                response+="The prices are "
                for product in available:
                    response+=str(product[1])
                    if(product!=available[len(available)-1]):
                        response+=","        
                response+=". "
            else:
                verb=""
                if response[-1]=="s":
                    verb=" are "
                else:
                    verb=" is "

                response+=verb
                response+="available. The price is "
                response+=str(available[0][1])+". "

            


        #response for unavailable products
        if len(unavailable)>0:
            for product in unavailable:
                response+=product
                if(product!=unavailable[len(unavailable)-1]):
                    response+=","
            
            if len(unavailable)>1:
                response+=" are not available."
            else:
                verb=""
                if response[-1]=="s":
                    verb=" are "
                else:
                    verb=" is "
                response+=verb
                response+="not available."


        # if response is empty then there are no entities or spellings are wrong
        if(len(response)==0):
            response = "These products are not available. Please make sure spellings are correct."

        dispatcher.utter_message(text=response)

        # SlotSet is used to hold information of available product 
        # if user asks to place order after this action then
        # this information can be used to place order

        return [SlotSet("requested_products", available)]

class ActionPlaceOrder(Action):

    def name(self) -> Text:
        return "action_place_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # fetch all the products that user asked in previous actoin
        products = tracker.get_slot("requested_products")
        
        # fetch entities from current message
        entities = tracker.latest_message['entities']
        
        # if user doesn't specified any products throughout the conversation and asks to place order
        if len(products)==0 and len(entities)==0:
            dispatcher.utter_message(text="Please specify products that you want to purchase.")
            return []

        # filter products if user selected some products from requested products in current message
        response = ""
        if len(products)>0 and len(entities)>0:
            filteredProducts =[]
            totalPrice = 0
            reqProducts = []
            for entity in entities:    
                if entity['entity']=='product':
                    reqProducts.append(entity['value'])
            
            response="Your requested products are "
            for product in products: #product[0]:name product[1]:price product[2]:quantity
                if product[0] in reqProducts:
                    response+=str(product[2])
                    response+="kg "
                    response+=product[0]
                    if product[0]!=products[len(products)-1][0]:
                        response+=", "
                    else:
                        response+=". "
                    totalPrice+=product[1]
                    filteredProducts.append(product)       

            response+="The total price is: "
            response+=str(totalPrice)
            response+=". Should I place your order?"
        
        elif len(products)>0:
            # if user ask to place order for all requested products
            totalPrice=0
            response="Your requested items are "
            for product in products: #product[0]:name product[1]:price product[2]:quantity
                response+=str(product[2])
                response+="kg "
                response+=product[0]
                if product[0]!=products[len(products)-1][0]:
                    response+=", "
                else:
                    response+=". "
                totalPrice+=product[1]       

            response+="The total price is: "
            response+=str(totalPrice)
            response+=". Should I place your order?"
        
        else:
            response="Please specify products that you want to purchase."

        # for entity in entities:
        #     print(entity)

        # for item in tracker.slots:
        #     print(item)
        # products = tracker.slots["product"]
        
        # print(products)
        dispatcher.utter_message(text=response)

        return []

class ActionConfirmOrder(Action):

    def name(self) -> Text:
        return "action_confirm_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        data = tracker.get_slot("requested_products")
        if len(data)==0:
            dispatcher.utter_message(text="Great! carry on")
            return []

        obj = {"data":data}
        print(obj)
        status = requests.post("http://127.0.0.1:5000/postOrder",json=obj)
        print(status)
        dispatcher.utter_message(text="Your order has been placed!")

        return []