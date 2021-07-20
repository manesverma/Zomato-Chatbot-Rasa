from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import zomatopy
import json


response=""

class ActionSearchRestaurants(Action):
    def name(self):
        return 'action_search_restaurants'
        
    def run(self, dispatcher, tracker, domain):
        config={ "user_key":"7d5e682455b1240601aa9d3204d37f09"}
        zomato = zomatopy.initialize_app(config)
        loc = tracker.get_slot('location')
        cuisine = tracker.get_slot('cuisine')
        location_detail=zomato.get_location(loc, 1)
        d1 = json.loads(location_detail)
        lat=d1["location_suggestions"][0]["latitude"]
        lon=d1["location_suggestions"][0]["longitude"]
        cuisines_dict={'bakery':5,'chinese':25,'cafe':30,'italian':55,'biryani':7,'north indian':50,'south indian':85}
        results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 5)
        d = json.loads(results)
        response="Showing you top rated restaurants:"+"\n"
        if d['results_found'] == 0:
            response= "No restaurant found for your criteria"
            dispatcher.utter_message(response)
        else:           
            for restaurant in sorted(d['restaurants'], key=lambda x: x['restaurant']['user_rating']['aggregate_rating'], reverse=True): 
                #Getting Top 10 restaurants for chatbot response
                if((restaurant['restaurant']['average_cost_for_two'] < 300)):
                    response=response+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+ " has been rated "+ restaurant['restaurant']['user_rating']['aggregate_rating']+"."
                    response=response+" And the average price for two people is: "+ str(restaurant['restaurant']['average_cost_for_two'])+"\n"
                #    count = count + 1
                elif((restaurant['restaurant']['average_cost_for_two'] >= 300) and (restaurant['restaurant']['average_cost_for_two'] <= 700)):
                    response=response+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+ " has been rated "+ restaurant['restaurant']['user_rating']['aggregate_rating']+"\n"
                    response=response+" And the average price for two people is: "+ str(restaurant['restaurant']['average_cost_for_two'])+"\n"
                #    count = count + 1                        
                elif((restaurant['restaurant']['average_cost_for_two'] > 700)):
                    response=response+ restaurant['restaurant']['name']+ " in "+ restaurant['restaurant']['location']['address']+ " has been rated "+ restaurant['restaurant']['user_rating']['aggregate_rating']+"\n"
                    response=response+" And the average price for two people is: "+ str(restaurant['restaurant']['average_cost_for_two'])+"\n"
                #    count = count + 1           
                #if(count==5):
                #    dispatcher.utter_message(response)
        #if(count<5 and count>0):
        #    dispatcher.utter_message(response)
        #if(count==0):
        #    response = "Sorry, No results found for your criteria. Would you like to search for some other restaurants?"
        #    dispatcher.utter_message(response)
        dispatcher.utter_message(str(response))
		#return [SlotSet('emailbody',response)]

        


class ActionCheckLocation(Action):

    def name(self):
        return 'check_location'

    def run(self, dispatcher, tracker, domain):
        loc = tracker.get_slot('location')
        
        cities=['Ahmedabad', 'Bangalore', 'Chennai', 'Delhi', 'Hyderabad', 'Kolkata', 'Mumbai', 'Pune',
        'Agra', 'Ajmer', 'Aligarh', 'Amravati', 'Amritsar', 'Asansol', 'Aurangabad', 'Bareilly',
        'Belgaum', 'Bhavnagar', 'Bhiwandi', 'Bhopal', 'Bhubaneswar', 'Bikaner', 'Bokaro Steel City',
        'Chandigarh', 'Coimbatore', 'Cuttack', 'Dehradun', 'Dhanbad', 'Durg-Bhilai Nagar', 'Durgapur',
        'Erode', 'Faridabad', 'Firozabad',    'Ghaziabad', 'Gorakhpur', 'Gulbarga', 'Guntur', 'Gurgaon',
        'Guwahati', 'Gwalior', 'Hubli-Dharwad', 'Indore', 'Jabalpur', 'Jaipur', 'Jalandhar', 'Jammu', 'Jamnagar',
        'Jamshedpur', 'Jhansi', 'Jodhpur', 'Kannur', 'Kanpur', 'Kakinada', 'Kochi', 'Kottayam', 'Kolhapur', 'Kollam',
        'Kota', 'Kozhikode', 'Kurnool', 'Lucknow', 'Ludhiana', 'Madurai', 'Malappuram', 'Mathura', 'Goa', 'Mangalore',
        'Meerut', 'Moradabad', 'Mysore', 'Nagpur', 'Nanded', 'Nashik', 'Nellore', 'Noida', 'Palakkad', 'Patna',
        'Pondicherry', 'Prayagraj', 'Raipur', 'Rajkot', 'Rajahmundry', 'Ranchi', 'Rourkela', 'Salem', 'Sangli',
        'Siliguri', 'Solapur', 'Srinagar', 'Sultanpur', 'Surat', 'Thiruvananthapuram', 'Thrissur', 'Tiruchirappalli',
        'Tirunelveli', 'Tiruppur', 'Ujjain', 'Bijapur', 'Vadodara', 'Varanasi', 'Vasai-Virar City', 'Vijayawada']
        
        cities_lower=[x.lower() for x in cities]
        
        if loc.lower() not in cities_lower:
            dispatcher.utter_message("Sorry, we don’t operate in this city. Can you please specify some other location")
        return     		

