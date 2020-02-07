import json, requests

def genlatlong(marketCity, marketState, map_subscription_key):

    mapsearchurl = "https://atlas.microsoft.com/search/address/json?"
    map_subscription_key = "subscription-key=" + map_subscription_key
    map_api_version = "&api-version=1.0"
    map_query = "&query=" + marketCity + ',' + marketState
    mapurl = mapsearchurl + map_subscription_key + map_api_version + map_query
    responsemap = requests.get(mapurl)
    if responsemap.status_code == 200:
        map_latlong_valid = True
        y = json.loads(responsemap.text)
        map_latitude = (y["results"][0]["position"]["lat"])
        map_longitude = (y["results"][0]["position"]["lon"])

    else:
        map_latlong_valid = False

    map_latlong = {"map_latitude" : map_latitude, "map_longitude" : map_longitude, "map_latlong_valid" : map_latlong_valid}

    return map_latlong

