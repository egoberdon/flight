import sqlite3 as sql
import googlemaps, urllib, json, math
from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_url_path='')

''' Home Page '''
@app.route('/')
def index():
    return render_template('index.html')

''' Results Page '''
@app.route('/results')
def list():
   conn = sql.connect("database.db")
   conn.row_factory = sql.Row
   cur = conn.cursor()
   cur.execute("select * from places")
   rows = cur.fetchall();
   return render_template("results.html",rows = rows)

'''Processes input from jquery post in index.html'''
@app.route('/input', methods=['POST'])
def process_input():
    category = request.form["category"]
    distance = request.form["distance"]
    start   = request.form["start"]
    places(category, distance, start)
    return "Successfully processed, redirecting to results page"

'''Gets Google API Key from Key file in this directory'''
def getKey():
    with open('key', 'r') as f:
        key = f.read().strip()
    return key

'''Uses Google Maps API to geocode the starting location
returning a 3 tuple of name, latitude, and longitude'''
def center(location):
    gmaps = googlemaps.Client(key=getKey())
    geocode_result = gmaps.geocode(location)
    latitude = geocode_result[0]['geometry']['location']['lat']
    longitude = geocode_result[0]['geometry']['location']['lng']
    return (location,latitude, longitude) #3-tuple of name latitude and location

'''Uses Google Places API to find all locations within designated radius, creates url with given information'''
def places(category, distance, start_loc):
    locations = []
    start = center(start_loc)
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
    latitude = start[1]
    longitude = start[2]
    distance = str(float(distance) * 1609.34 )# convert from miles to meters and then convert type to string
    url = url + str(latitude) +',' + str(longitude) + '&rankBy=distance&radius=' + distance + '&keyword=' + category + '&key=' + getKey()
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    for place in data['results']:
        curLat = place['geometry']['location']['lat']
        curLng = place['geometry']['location']['lng']
        current = (place['name'], curLat, curLng) #3-tuple of name latitude and location
        locations.append(current)
    output = []
    output.append(start)
    total = 0 # total distance
    nearest_neighbor(start, locations, output, total)

'''
Recieves an array of 3-tuples (locations) that are compared against start to find the nearest neighbor
Recursively runs until the locations array is empty
at this time the output array is full and the database can be filled
the first item in the database is a special row to hold the total distance information
'''
def nearest_neighbor(start, locations, output, total):
    if len(locations) == 0:
        conn = sql.connect('database.db')
        conn.execute("DROP TABLE IF EXISTS places") # only want to keep one set of results at a time, so clear if an old table is around
        conn.execute("CREATE TABLE IF NOT EXISTS places (name TEXT, lat REAL, lng REAL, total REAL)")
        conn.execute("INSERT INTO places (name, total) VALUES (?, ?)", ("total", total)) #storing total distance to table
        for loc in output: #type elements and add to array
            name = str(loc[0])
            lat = float(loc[1])
            lng = float(loc[2])
            conn.execute("INSERT INTO places (name, lat, lng) VALUES (?, ?, ?)", (name, lat, lng))
        conn.commit()
        conn.close()
    else:
        lat = start[1]
        lng = start[2]
        #set min_distance and min_index to first, item then check the others (if any exist)
        min_distance = math.hypot(locations[0][1] - lat, locations[0][2] - lng) #start the min distance & index with the first item, which we know exists due to the base case check
        min_index = 0
        i = 1 #we've already checked the zero index, so we start at 1
        while (i < len(locations)):
            cur_lat = locations[i][1]
            cur_lng = locations[i][2]
            distance = math.hypot(cur_lat - lat, cur_lng - lng) #calculates distance between two points
            if (distance < min_distance): #update min_index and min_distance if a new smallest distance has been found
                min_index = i
                min_distance = distance
            i += 1
        total += min_distance #add the min_distance to the total distance, ensuring we only travel the shortes distance at every step
        start = locations.pop(min_index) # remove the the min_index item from locations and set it to start
        output.append(start) # append the new start to the output array
        nearest_neighbor(start, locations, output, total) # recursively call the function

if __name__ == '__main__':
    app.run(debug=True, port=8000)
