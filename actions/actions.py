# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk.executor import ActionExecutor
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

class ActionAcceptOffer(Action):

    def name(self) -> Text:
        return "action_accept_offer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        offer = tracker.get_slot("counterOffer")
        netDiscount = tracker.get_slot("netDiscount")
        discountReceived = tracker.get_slot("netDiscountReceived")
        offer = int(offer)
        netDiscount-=offer
        if discountReceived:
            discountReceived+=offer
        else:
            discountReceived=offer

        return [SlotSet("netDiscount",netDiscount),SlotSet("netDiscountReceived",discountReceived)]

class ActionUpdateCart(Action):

    def name(self) -> Text:
        return "action_remove_or_update_items"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        products = {}
        entities = tracker.latest_message['entities']

        #Map product with it's quantity
        productNames = [] 
        quantities = []
        for entity in entities:
            if entity['entity']=='quantity':
                qty = re.sub(r"\D","",entity['value'])
                quantities.append(int(qty))
            else:
                productNames.append(entity['value'])

        j=0
        for i in range(0,len(productNames)):
            if j<len(quantities):
                products[productNames[i]]=quantities[j]
                j+=1
            else:
                products[productNames[i]]=-1

        print(products)
        
        #update cart accordingly
        cart = tracker.get_slot("requested_products")
        print(cart)
        newCart = []
        for i in range(0,len(cart)):
            if cart[i][0] in products:
                newValue = products[cart[i][0]]
                if newValue == -1:
                    continue
                elif newValue <= cart[i][2]:
                    perUnitPrice = cart[i][1]/cart[i][2]
                    cart[i][2]-=newValue
                    cart[i][1]=(cart[i][2]*perUnitPrice)
            newCart.append(cart[i])

        print(cart)
        discount = tracker.get_slot("discount")
        netDiscountReceived = tracker.get_slot("netDiscountReceived")
        netDiscount,netDiscountReceived = adjustDiscounts(newCart,discount,netDiscountReceived)

        dispatcher.utter_message(text="Your cart has been updated..")
        return [SlotSet("requested_products", newCart),SlotSet("netDiscount", netDiscount),SlotSet("netDiscountReceived",netDiscountReceived)]

class NegotiationByCounterOffers():

    def negotiate(self,dispatcher,requestedPrice,netDiscount,netDiscountReceived,cart):
        #calculate total amount
        tot=0
        for item in cart:
            tot+=item[1]

        requestedDiscount = tot-netDiscountReceived-requestedPrice
        counterOffer=None
        if requestedDiscount<=netDiscount:
            # offer accepted
            netDiscountReceived+=requestedDiscount
            netDiscount-=requestedDiscount
            
            
            # price after discount
            tot-=netDiscountReceived
            dispatcher.utter_message(text="Offer Accepted. Your total bill after discount would be "+str(round(tot,2)))

        else:
            canOffer = tot-netDiscount
            mid = int((canOffer+requestedPrice)/2)
            diff = canOffer-mid
            newOffer = canOffer+diff
            if newOffer>=(tot-netDiscountReceived):
                newOffer = int((canOffer+(tot-netDiscountReceived))/2)
            counterOffer = tot-netDiscountReceived-newOffer
            newOffer = str(newOffer)
            # offer rejected
            dispatcher.utter_message(text="Sorry, That's too low. I would be making no profit from this deal.")
            dispatcher.utter_message(text="How about "+newOffer+"?")
       
        return counterOffer,netDiscountReceived,netDiscount

class NegotiationByFinalOffer():
    
    def negotiate(self,dispatcher,requestedPrice,netDiscount,netDiscountReceived,cart):

        #calculate total amount
        tot=0
        for item in cart:
            tot+=item[1]

        requestedDiscount = tot-netDiscountReceived-requestedPrice

        if requestedDiscount<=netDiscount:
            # offer accepted
            netDiscountReceived+=requestedDiscount
            netDiscount-=requestedDiscount
            
            
            # price after discount
            tot-=netDiscountReceived
            dispatcher.utter_message(text="Offer Accepted. Your total bill after discount would be "+str(tot))

        else:
            # offer rejected
            dispatcher.utter_message(text="Sorry, That's too low. I would be making no profit from this deal. ")

       
        return None,netDiscountReceived,netDiscount


class ActionNegotiateOverall(Action):

    def name(self) -> Text:
        return "action_negotiate_overall"

    def ExtractPrice(self,tracker):
        entities = tracker.latest_message['entities']
        for entity in entities:
            if entity['entity']=='quantity':
                return int(entity['value'])
        return 0

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        requestedPrice = self.ExtractPrice(tracker)
        netDiscount = tracker.get_slot("netDiscount")
        netDiscountReceived = tracker.get_slot("netDiscountReceived")
        cart = tracker.get_slot("requested_products")

        # nego = NegotiationByFinalOffer()
        nego = NegotiationByCounterOffers()
        counterOffer,netDiscountReceived,netDiscount = nego.negotiate(dispatcher,requestedPrice,netDiscount,netDiscountReceived,cart)
        return [SlotSet("counterOffer",counterOffer),SlotSet("netDiscountReceived",netDiscountReceived),SlotSet("netDiscount",netDiscount)]


class ActionNegotiate(Action):

    def name(self) -> Text:
        return "action_negotiate"

    def ExtractProductsAndPrices(self , tracker):

        # fetching products and their desired prices or overall price
        entities = tracker.latest_message['entities']
        products = []
        product = []
        prices =  []
        
        for entity in entities:
            if entity['entity']=='product':
                product.append(entity['value'])
            else:
                prices.append(entity['value'])
        
        #connecting products with prices
        ind=len(product)-1
        for price in reversed(prices):
            if ind<0: break
            products.append([product[ind],int(price)])
            ind-=1

        return products

    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        productsInfo = self.ExtractProductsAndPrices(tracker)       
        cart = tracker.get_slot("requested_products")

        requestedDiscount=0
        # if(len(productsInfo)==1):
        #     # check if user wants overall discount
        #     if(productsInfo[0][1]=="-"):
        #         requestedDiscount = productsInfo[0][1]
        # else:
        print(productsInfo)
        #check how much discount user wants on each product        
        for product in productsInfo:
            name = product[0]
            desiredPrice = product[1]
            #search this product in cart to compute difference between actual price and requested price
            for item in cart:
                if item[0]==name:
                    requestedDiscount+=item[1]-desiredPrice
                    break
    
        netDiscount = tracker.get_slot("netDiscount")
        netDiscountReceived = tracker.get_slot("netDiscountReceived")

        #calculate total price
        tot=0
        for item in cart:
            tot+=item[1]

        if requestedDiscount<=netDiscount:
            # offer accepted
            netDiscountReceived+=requestedDiscount
            netDiscount-=requestedDiscount
            
            
            # price after discount
            tot-=netDiscountReceived
            dispatcher.utter_message(text="Offer Accepted. Your total bill after discount would be "+str(tot))

        else:
            # offer rejected
            
            dispatcher.utter_message(text="Sorry, I would be making no profit from this deal. However, if you purchase additional items, I can offer a greater discount. ")
       
        return [SlotSet("netDiscountReceived",netDiscountReceived),SlotSet("netDiscount",netDiscount)]

class ActionFetchDiscount(Action):

    def name(self) -> Text:
        return "action_fetch_discount"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #tracker.sender_id: fetches sender id from tracker object
        print(tracker.sender_id)
        uid = tracker.sender_id
        data = requests.get("http://localhost:5000/discount?uid="+uid)
        print(data.json())
        #for now setting discount to default value
        data = data.json()
        discount = data["discount"]
        print(discount)
        # discount=0.2
        return [SlotSet("discount", discount),SlotSet("netDiscount", 0),SlotSet("netDiscountReceived", 0)]

def adjustDiscounts(products,discount,netDiscountReceived):
    totDiscount=0
    for p in products:
        totalPrice = p[1]
        maxDiscountPerProduct = p[3]
        discountOnUserType = maxDiscountPerProduct 
        if discount == "M":

            discountOnUserType = (discountOnUserType*100)/2
            discountOnUserType/=100

        elif discount == "L":
            discountOnUserType = (discountOnUserType*100)/4
            discountOnUserType/=100

        print("discountOnUserType: ",discountOnUserType)
        totDiscount+=(totalPrice*discountOnUserType)
    
    if netDiscountReceived>totDiscount:
        netDiscountReceived=totDiscount
        totDiscount=0
    else:
        totDiscount=totDiscount-netDiscountReceived
    
    print("netDiscount: ",totDiscount)
    print("netDiscountReceived: ",netDiscountReceived)
    return totDiscount,netDiscountReceived

class ActionProductQuery(Action):

    def name(self) -> Text:
        return "action_product_query"

    def extractProductsInfo(self,tracker):
        # extract all product names and their quantities
        # assuming user would give quantity for each product! else quantity extraction might be wrong
        products = []
        quantities = []
        entities = tracker.latest_message['entities']

        for entity in entities:    
            if entity['entity']=='quantity':
                quantities.append(entity['value'])
                print(entity['value'])
            else:
                products.append(entity['value'])

        cart = []
        j = 0
        print("Length of quantities: ",len(quantities))
        print("Length of products: ",len(products))
        for i in range(0,len(products)):
            if j<len(quantities):
                print("original string",quantities[j])
                qty = re.sub(r"[a-z]","",quantities[j])
                print("from regex: ",qty)
                j+=1
            else:
                qty = "1"
            cart.append([products[i],float(qty)])

         
        return cart

    def checkProductsAvailability(self,products):
        # check if products are available
        estoreProducts = requests.get("http://127.0.0.1:5000/products")
        estoreProducts = estoreProducts.json()
        # print(estoreProducts)
        

        available = []
        unavailable = []

        for product in products:
            name = product[0]
            qty = product[1]
            if name in estoreProducts and estoreProducts[name]["qty"]>=qty:
                    # product is available with required quantity
                    # calculate total price and append in available array
                    totalPrice = estoreProducts[name]["price"]*qty
                    maxDiscount = estoreProducts[name]["maxDiscount"]
                    available.append([name,totalPrice,qty,maxDiscount])
            else:
                # product is not available
                unavailable.append(name)
        # print(available)
        return available,unavailable

    def generateResponse(self,available,unavailable):
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
                response+=". Items are added to your cart."
            else:
                verb=""
                if response[-1]=="s":
                    verb=" are "
                else:
                    verb=" is "

                response+=verb
                response+="available. The price is "
                response+=str(available[0][1])+". Item is added to your cart."

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
            response = "Please specify products that you want to buy. Make sure spellings are correct."

        return response



    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:       
        
        products = self.extractProductsInfo(tracker)
        available,unavailable = self.checkProductsAvailability(products)
        print(available)
        print(unavailable)
        response = self.generateResponse(available,unavailable)
        dispatcher.utter_message(text=response)

        # SlotSet is used to hold information. In this case requested_products
        # hold updated information of cart(i.e what products user selected so far) 
        # if user asks to place order then this slot can be used to place order
        cart = tracker.get_slot("requested_products")
        print(cart)
        # updating cart items
        if cart:
            if len(cart)>0:
                for p in cart:
                    f=1
                    # checking for duplicate values, only appending old cart items that are not
                    # in current requested items
                    for i in range(len(available)):
                        if p[0] == available[i][0]:
                            f=0
                            break
                    if(f):
                        available.append(p)

        #adjust discounts
        discount = tracker.get_slot("discount")
        netDiscountReceived = tracker.get_slot("netDiscountReceived")
        netDiscount,netDiscountReceived = adjustDiscounts(available,discount,netDiscountReceived) 
        
        return [SlotSet("requested_products", available),SlotSet("netDiscount", netDiscount),SlotSet("netDiscountReceived",netDiscountReceived)]
        


class ActionPlaceOrder(Action):

    def name(self) -> Text:
        return "action_place_order"

    def filterProducts(self,entities,products):
        # filter products if user selected some products from requested products in current message
        response = ""
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

        return filteredProducts,totalPrice,response

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        products = [] 
        entities = []

        # fetch all the products that user asked in previous actoin
        # checks are used to handle "none" value cases
        if tracker.get_slot("requested_products"):
            products = tracker.get_slot("requested_products")
        
        # fetch entities from current message
        if tracker.latest_message['entities']:
            entities = tracker.latest_message['entities']
        
        # if user doesn't specified any products throughout the conversation and asks to place order
        if  (len(products)==0 and len(entities)==0):
            dispatcher.utter_message(text="Please specify products that you want to purchase.")
            return []

        # filter products if user selected some products from requested products in current message
        response = ""
        netDiscountReceived = tracker.get_slot("netDiscountReceived")
        print(netDiscountReceived)
        if len(products)>0 and len(entities)>0:   

            filteredProducts,totalPrice,response = self.filterProducts(entities,products)
            
            #adjust discounts
            discount = tracker.get_slot("discount")
            netDiscountReceived = tracker.get_slot("netDiscountReceived")
            netDiscount,netDiscountReceived = adjustDiscounts(filteredProducts,discount,netDiscountReceived)
            
            response+="The total price is: "
            response+=str(totalPrice-netDiscountReceived)
            response+=". Should I place your order?"
            
            dispatcher.utter_message(text=response)
            
            return [SlotSet("requested_products", filteredProducts),SlotSet("netDiscount", netDiscount),SlotSet("netDiscountReceived",netDiscountReceived)]
        
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
            response+=str(totalPrice-netDiscountReceived)
            response+=". Should I place your order?"
        
        else:
            response="Please specify products that you want to purchase."

   
        dispatcher.utter_message(text=response)

        return []

class ActionConfirmOrder(Action):

    def name(self) -> Text:
        return "action_confirm_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        data = tracker.get_slot("requested_products")
            
        if data:
            obj = {"data":data,"userId":tracker.sender_id,"netDiscountReceived":tracker.get_slot("netDiscountReceived")}
            print(obj)
            status = requests.post("http://127.0.0.1:5000/postOrder",json=obj)
            print(status)
            dispatcher.utter_message(text="Your order has been placed!")
        else:
            dispatcher.utter_message(text="Great! carry on")
        
        return [SlotSet("netDiscountReceived",0),SlotSet("netDiscount",0),SlotSet("requested_products",None),SlotSet("counterOffer",None)]
        