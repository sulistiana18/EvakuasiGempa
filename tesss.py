###import reverse_geocoder as rg
#import pprint
from random import randrange
import requests

bandungLocation = "Yogyakarta"
skalaGempa = 0 # skala gempa
ifTsunami = True # apakah akan ada tsunami

################ GET USER LOCATION ###############

r = requests.get('https://get.geojs.io/')

ip_requests = requests.get('https://get.geojs.io/v1/ip.json')
ipAdd = ip_requests.json()['ip']
##print(ipAdd)

url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
geo_requests = requests.get(url)
geo_data = geo_requests.json()

userLocation = (geo_data['latitude'],geo_data['longitude']) # get user location

##################################################

def getCity():
    userCity = geo_data['city']
    return (userCity)

def getRegion():
    userRegion = geo_data['region']
    return (userRegion)

def getCountry():
    userCountry = geo_data['country']
    return (userCountry)

'''
def reverseGeocode(coordinates):
    result = rg.search(coordinates)
     
    # result is a list containing ordered dictionary.
    pprint.pprint(result)
'''

def dist_between_two_lat_lon(*args):
    from math import asin, cos, radians, sin, sqrt
    lat1, lat2, long1, long2 = map(radians, args)

    dist_lats = abs(lat2 - lat1) 
    dist_longs = abs(long2 - long1) 
    a = sin(dist_lats/2)**2 + cos(lat1) * cos(lat2) * sin(dist_longs/2)**2
    c = asin(sqrt(a)) * 2
    radius_earth = 6378 # the "Earth radius" R varies from 6356.752 km at the poles to 6378.137 km at the equator.
    return c * radius_earth


def findClosestShelter(data, v):
    try:
        return min(data, key=lambda p: dist_between_two_lat_lon(v[0],p[0],v[1],p[1]))
    except TypeError:
        print('Not a list or not a number.')


mcd_dago = [10, 45.44]
kebon_binatang = [50, -9]
 
shelterList = [mcd_dago, kebon_binatang]
userLocation = [-6.914744, 107.609810]


# def coordinateToLocation(data, c):
#     try:
#         return min (data, key=lambda p: ifLocationSame(c[0], p[0], c[1], p[1]))
#     except TypeError:
#         print('Not a list or not a number')


def stayAtHome():
    print("Tidak perlu ke Shelter")
 

# modelnya gini kira2


def model():
    if getCity() == bandungLocation:
        print ("Lokasi anda: "+ getCity()+","+ getCountry())
        skalaGempa = randrange(10)
        if skalaGempa >= 6:
            if ifTsunami == True:
                x = findClosestShelter(shelterList, userLocation)
                print(x)
                #print(coordinateToLocation(shelterList,x))
                # print(ifLocationSame(shelterList, x))
                print("Info Gempa: "+skalaGempa)
            else:
                stayAtHome()
                print("Info Gempa: "+skalaGempa)
        else:
            stayAtHome()
            print("Info Gempa: "+skalaGempa)
    else:
        print ("Anda tidak di bandung")
        print (" ")
        print ("Anda berada di: "+getCity())
