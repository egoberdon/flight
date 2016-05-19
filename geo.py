import googlemaps

def getKey():
    with open('key', 'r') as f:
        key = f.read().strip()
    return key

def center():
    gmaps = googlemaps.Client(key=getKey())
    geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
    latitude = geocode_result[0]['geometry']['location']['lat']
    longitude = geocode_result[0]['geometry']['location']['lng']
    return (latitude, longitude)

def main():
    print center()

main()
