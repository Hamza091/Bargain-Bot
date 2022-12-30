# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import re
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
                    available.append([name,totalPrice])
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

        return []