"""
Author : Rohan Chandra 

Python script to use the census geocoder to find the latitude and longitude of the whitehouse, ask the user for an address,
find the latitude and longitude of that address, and print the distance between the two locations in miles.

"""

import urllib.request, urllib.parse, urllib.error
import json
import math

#get whitehouse latitude and longitude
serviceurl = 'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?'  #geocoder access link
whitehouse = '1600 Pennsylvania Avenue, Washington, DC'          #onelineaddress of whitehouse 
whitehouse_url = serviceurl + urllib.parse.urlencode({'address': whitehouse}) + '&benchmark=9&format=json'  #encode
wh = urllib.request.urlopen(whitehouse_url)
wh_data = wh.read().decode()

try:
    wh_js = json.loads(wh_data)
except:
    wh_js = None

wh_lat = wh_js["result"]["addressMatches"][0]["coordinates"]["x"]       #whitehouse latitude
wh_lng = wh_js["result"]["addressMatches"][0]["coordinates"]["y"]       #whitehouse longitude 

while True:
    #collect the user's street, city and state
    street, city, state = input('Enter your Street: '), input('Enter your city: '), input('Enter your state: ')
    if len(street) < 1 or len(city) < 1 or len(state) < 1 :
        print("You did not enter all 3 required fields!(street, city and state)")
        if input('Press any key to enter another address or Y to quit: ').upper() == 'Y' :
            break
        continue   
    
    #get entered address latitude and longitude
    address = f'{street}, {city}, {state}'
    url = serviceurl + urllib.parse.urlencode({'address': address}) + '&benchmark=9&format=json'
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    
    try:
        js = json.loads(data)
    except:
        js = None
    
    try :
        if js["result"]["addressMatches"] == [] :   #if no matching address found by geocoder                
            raise IndexError
    
    except IndexError :
        print(f'No matching address found for {street}, {city}, {state} .Check the address.')
        if input('Press any key to enter another address or Y to quit: ').upper() == 'Y' :
            break
        
    else :
        
        lat = js["result"]["addressMatches"][0]["coordinates"]["x"]       # entered address latitude    
        lng = js["result"]["addressMatches"][0]["coordinates"]["y"]       # entered address longitude 

        #calculate the distance between the two locations in miles
        dlat = math.radians(lat-wh_lat)
        dlon = math.radians(lng-wh_lng)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(wh_lat)) \
        * math.cos(math.radians(lat)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        radius = 3963 - 13 * math.sin(math.radians(lat))
        d = radius * c
        
        print('The distance between the entered address and the White house is about %.0f miles.' % d)
        if input('Press any key to enter another address or Y to quit: ').upper() == 'Y' :
            break
        
      
       
    
    


        
