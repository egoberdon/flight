import googlemaps, urllib, json, math

def getKey():
    with open('key', 'r') as f:
        key = f.read().strip()
    return key

def center():
    gmaps = googlemaps.Client(key=getKey())
    center = '134 West 26th Street, New York, NY 10001'
    geocode_result = gmaps.geocode(center)
    latitude = geocode_result[0]['geometry']['location']['lat']
    longitude = geocode_result[0]['geometry']['location']['lng']
    return (center,latitude, longitude) #3-tuple of name latitude and location

def places():
    locations = []
    start = center()
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
    latitude = start[1] #-33.86879
    longitude = start[2] #151.194217
    distance  = '500'
    category = 'thai'
    url = url + str(latitude) +',' + str(longitude) + '&rankBy=distance&radius=' + distance + '&keyword=' + category + '&key=' + getKey()
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    for place in data['results']:
        curLat = place['geometry']['location']['lat']
        curLng = place['geometry']['location']['lng']
        print place['name']
        current = (place['name'], curLat, curLng) #3-tuple of name latitude and location
        locations.append(current)
        #distance = math.hypot(curLat - latitude, curLng - longitude)
    output = []
    output.append(start)
    total = 0 # total distance
    return nearest_neighbor(start, locations, output, total)

'''
recieves an array of 3-tuples where the first element is the one to compare against
when array is length one return output array
'''
def nearest_neighbor(start, locations, output, total):
    if len(locations) == 0:
        print 'Total distance is: ' + str(total)
        print 'Locations in order visited:\n'
        for loc in output:
            print str(loc[0])
    else:
        lat = start[1]
        lng = start[2]
        min_distance = math.hypot(locations[0][1] - lat, locations[0][2] - lng) #start the min distance & index with the first item, which we know exists due to the base case check
        i = 0
        min_index = 0
        while (i < len(locations)):
            cur_lat = locations[i][1]
            cur_lng = locations[i][2]
            distance = math.hypot(cur_lat - lat, cur_lng - lng)
            if (distance < min_distance):
                min_index = i
                min_distance = distance
            i += 1
        total += min_distance
        start = locations.pop(min_index)
        output.append(start)
        nearest_neighbor(start, locations, output, total)

if __name__ == '__main__':
    places()
