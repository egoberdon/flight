# flight

## Overview

This is a web application that takes user input and calculates the shortest flight path (as the crow flies)
to all matching locations in the given area.

### Home Page

The home page has three text input boxes.
  + The first one takes a type of place. This would be something like "Thai" for Thai restaurants (this is loaded into the Google Places API as a _keyword_)
  + The second input box takes a distance in miles (this is converted to meters for the Google Places API)
  + The third box takes a starting address like '125 E 11th St, New York, NY 10003' (this is geocoded using the Google Maps API, which returns the location to then be used by the Places API)

### Results

The results page lists all the locations in order visited (plus their latitude and longitude). The address entered on the home page is listed as the first location. The total distance for the entire flight is given. The units for this distance is in latitudes/longitudes which is
the result of the `math.hypot()` function that calculates the distance between points.

### Algorithmic Complexity

Finding the shortest path as the crow flies to various locations is a manifestation of the
Traveling Salesperson Problem (TSP).
To approximate TSP I use the Nearest Neighbor Algorithm (_see the nearest_neighbor function in server.py_). The Nearest Neighbor algorithm is a simple and straightforward
approximation that works relatively well. It recursively picks the nearest location to the start,
sets that as the new location then repeats the process. The run-time for this implementation is O(N^2): O(N)
to find the nearest neighbor, nested in another O(N) to iterate through all locations.

## Technologies

+ Flask - python microframework used for server
+ SQLite3 - used for storing places (names, latitudes, and longitudes)
+ BackboneJS - Used for event handling on the front end
+ Google Maps API - Used for geocoding starting location (_see center function in server.py_)
+ Google Places API - Used to find locations in given radius (_see places function in server.py_)
+ Twitter Bootstrap - used for styles and glyphicons

## Requirements

+ Python 2.7 or later
+ [Google Maps for Python] (https://github.com/googlemaps/google-maps-services-python google-maps-services-python)
+ Google API Key for both Maps and Places
+ All required js, css, and fonts files are located in the static folder

## Instructions
+ clone/download repo
+ `cd flight` into root directory
+ make a file called key that contains only your Google API Key
+ run `python server.py` in terminal
+ go to http://127.0.0.1:8000/ to see home page
