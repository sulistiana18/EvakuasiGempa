###import reverse_geocoder as rg
#import pprint
from random import randrange
import requests

from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from flask import Flask, send_from_directory
from pywebio.input import *
from pywebio.output import *
import argparse
from pywebio import start_server

app = Flask(__name__)

##bandungLocation = "Yogyakarta"
bandungLocation = "Bandung"
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


mcd_dago = [-6.884905429718143, 107.61343477064133]
kebon_binatang = [-6.889494010930266, 107.60777111436555]
masjid_pusdai = [-6.899779609038424, 107.62589145632269]
trans_studio = [-6.924891899683676, 107.63648962766213]
aston_pasteur = [-6.8935598412797345, 107.58723032879244]
bandara_husen = [-6.903314719663762, 107.57321285669948]
starbucks_setiabudhi = [-6.861120413849395, 107.59541762811227]
 
shelterList = [mcd_dago, kebon_binatang, masjid_pusdai, trans_studio, aston_pasteur, bandara_husen, starbucks_setiabudhi]


# def coordinateToLocation(data, c):
#     try:
#         return min (data, key=lambda p: ifLocationSame(c[0], p[0], c[1], p[1]))
#     except TypeError:
#         print('Not a list or not a number')


def stayAtHome():
    print("Tidak perlu ke Shelter")
 

# modelnya gini kira2

if getCity() == bandungLocation:
    style(put_text("Lokasi anda: "+ getCity()+","+ getCountry()), 'color:red')
    skalaGempa = randrange(10)
    if skalaGempa >= 6:
        if ifTsunami == True:
            x = findClosestShelter(shelterList, userLocation)
            put_text("Info Gempa: "+str(skalaGempa)+ " SR\n" + "\nBerpotensi Tsunami" + "\n" + "\nSaran: " + x)
            #print(coordinateToLocation(shelterList,x))
            # print(ifLocationSame(shelterList, x))
        else:
            put_text("Info Gempa: "+str(skalaGempa)+" SR\n" + "\nTidak Berpotensi Tsunami" + "\n" + "\nSaran: Tidak perlu ke Shelter!" )
    else:
        put_text("Info Gempa: "+str(skalaGempa)+ " SR\n" + "Tidak Berpotensi Tsunami" + "\n" + "Saran: Tidak perlu ke Shelter!" )
else:
    put_text("Anda Tidak di Bandung")



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(getCity, port=args.port)
