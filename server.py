import sqlite3 as sql
import googlemaps, urllib, json, math
from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def list():
   conn = sql.connect("database.db")
   conn.row_factory = sql.Row
   cur = conn.cursor()
   cur.execute("select * from places")
   rows = cur.fetchall();
   return render_template("results.html",rows = rows)

@app.route('/input', methods=['POST'])
def process_input():
    category = request.form["category"]
    distance = request.form["distance"]
    start   = request.form["start"]
    places(category, distance, start)
    return "Category is %s, Distance is %s, Start is %s." % (category, distance, start)

def getKey():
    with open('key', 'r') as f:
        key = f.read().strip()
    return key

def center(location):
    gmaps = googlemaps.Client(key=getKey())
    #location = '134 West 26th Street, New York, NY 10001'
    geocode_result = gmaps.geocode(location)
    latitude = geocode_result[0]['geometry']['location']['lat']
    longitude = geocode_result[0]['geometry']['location']['lng']
    return (location,latitude, longitude) #3-tuple of name latitude and location

def places(category, distance, start_loc):
    locations = []
    start = center(start_loc)
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='
    latitude = start[1]
    longitude = start[2]
    #distance  = '500'
    #category = 'thai'
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
recieves an array of 3-tuples where the first element is the one to compare against
when array is length zero return output array
'''
def nearest_neighbor(start, locations, output, total):
    if len(locations) == 0:
        # print 'Total distance is: ' + str(total)
        # print 'Locations in order visited:\n'
        conn = sql.connect('database.db')
        conn.execute("DROP TABLE IF EXISTS places") # only want to keep one set of results at a time
        conn.execute("CREATE TABLE IF NOT EXISTS places (name TEXT, lat REAL, lng REAL)")
        for loc in output:
            name = str(loc[0])
            lat = float(loc[1])
            lng = float(loc[2])
            conn.execute("INSERT INTO places (name, lat, lng) VALUES (?, ?, ?)", (name, lat, lng))
        conn.commit()
        conn.close()
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
    app.run(debug=True, port=8000)
