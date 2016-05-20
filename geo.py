import googlemaps, urllib, json, math

def getKey():
    with open('key', 'r') as f:
        key = f.read().strip()
    return key

def center():
    gmaps = googlemaps.Client(key=getKey())
    geocode_result = gmaps.geocode('134 West 26th Street, New York, NY 10001')
    latitude = geocode_result[0]['geometry']['location']['lat']
    longitude = geocode_result[0]['geometry']['location']['lng']
    return (latitude, longitude)

def places():
    total = 0
    loc = center()
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
    latitude = loc[0] #-33.86879
    longitude = loc[1] #151.194217
    distance  = '500'
    category = 'thai'
    url = url + str(latitude) +',' + str(longitude) + '&rankBy=distance&radius=' + distance + '&keyword=' + category + '&key=' + getKey()
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    for place in data['results']:
        print place['name']
        curLat = place['geometry']['location']['lat']
        curLng = place['geometry']['location']['lng']
        distance = math.hypot(curLat - latitude, curLng - longitude)
        total+= distance
        print distance
        # print '\t' + str(place['geometry']['location']['lat'])
        # print '\t' + str(place['geometry']['location']['lng'])
    print 'Total distance is: ' + str(total)
    
places()
