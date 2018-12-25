# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 09:52:42 2018

@author: com-ftrojan
"""
import numpy as np
import pandas as pd
import requests
import geocoder

# https://stackoverflow.com/questions/19513212/can-i-get-the-altitude-with-geopy-in-python-with-longitude-latitude/24780640#24780640
# script for returning elevation from lat, long, based on open elevation data
# which in turn is based on SRTM
def get_elevation(lat, long):
    query = "https://api.open-elevation.com/api/v1/lookup?locations=%.7f,%.7f" % (lat, long)
    r = requests.get(query).json()  # json object, various ways you can extract value
    # one approach is to use pandas json functionality:
    elevation = pd.io.json.json_normalize(r, 'results')['elevation'].values[0]
    return elevation

def get_coords(text):
    """ Returns (latitude, longitude, elevation) triple geocoded text. """
    g = geocoder.osm(text)
    lat = g.json['lat']
    lon = g.json['lng']
    print("%.4f, %.4f" % (lat, lon))
    h = get_elevation(lat, lon)
    return (lat, lon, h)

g = geocoder.arcgis('Lysa hora, okres Frydek')
g.json

g = geocoder.yahoo('Lysa hora, okres Frydek')
g.json

h = get_elevation(g.json['lat'], g.json['lng'])

get_coords('Lysa hora, okres Frydek')

# https://cgiarcsi.community/data/srtm-90m-digital-elevation-database-v4-1/
# http://www.viewfinderpanoramas.org/dem3.html

graphhopper_api_key = "3aa82fd4-5229-4983-9ec3-27a49339cd4e"
geocode_url = "https://graphhopper.com/api/1/geocode?q=berlin&locale=de&debug=true&key=%s" % graphhopper_api_key
r = requests.get(geocode_url).json()

geocode_url = "https://graphhopper.com/api/1/geocode?q=lysa hora&locale=cs&debug=true&key=%s" % graphhopper_api_key
r = requests.get(geocode_url).json()

rtrue = r['hits'][1]
xy = "%.7f, %.7f" % (rtrue['point']['lat'], rtrue['point']['lng'])

addel_url = "https://graphhopper.com/api/1/route?point=%s&point=%s&elevation=true&points_encoded=flase&vehicle=car&locale=de&key=%s" % (xy, xy, graphhopper_api_key)
r2 = requests.get(addel_url).json()
res = r2['paths'][0]['points']['coordinates'][0]
h = res[2]

def gh_coords(text):
    gh_key = "3aa82fd4-5229-4983-9ec3-27a49339cd4e"
    url1 = "https://graphhopper.com/api/1/geocode?q=%s&locale=en&debug=true&limit=20&key=%s" % (text, gh_key)
    r1 = requests.get(url1).json()
    hits = r1['hits']
    if len(hits) == 0:
        print("%s not found" % text)
        return None
    else:
        print("%d hits for %s found." % (len(hits), text))
        res = list()
        for i in range(len(hits)):
            hit = hits[i]
            lat = hit['point']['lat']
            lon = hit['point']['lng']
            xy = "%.7f, %.7f" % (lat, lon)
            url2 = "https://graphhopper.com/api/1/route?point=%s&point=%s&elevation=true&points_encoded=flase&vehicle=car&locale=de&key=%s" % (xy, xy, gh_key)
            r2 = requests.get(url2).json()
            #print(r2)
            if 'message' in r2.keys():
                print("%d: (%.4f,%.4f,NA) %s/%s/%s" % (i, lat, lon, hit['country'], hit['city'], hit['name']))
                res.append((lat, lon, np.nan))
            else:
                elev = r2['paths'][0]['points']['coordinates'][0][2]
                print("%d: (%.4f,%.4f,%.0f) %s/%s/%s" % (i, lat, lon, elev, hit.get('country','NA'), hit.get('city','NA'), hit.get('name','NA')))
                res.append((lat, lon, elev))
    return res

xyh = gh_coords("lysa hora krasna")
xyh = gh_coords("praded")
xyh = gh_coords("snezka")
xyh = gh_coords("klinovec")
xyh = gh_coords("tok pribram obecnice")
xyh = gh_coords("leogang")
xyh = gh_coords("dachstein")
xyh = gh_coords("zugspitze")
xyh = gh_coords("sonnblick")
xyh = gh_coords("mont blanc")
xyh = gh_coords("mont ventoux")
xyh = gh_coords("bozi dar")
