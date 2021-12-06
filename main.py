import csv
import os
from pymongo import MongoClient
import pymongo

if __name__ == "__main__":
    mongo_port = os.environ['MONGO_PORT']
else:
    mongo_port = 27017

client = MongoClient(port=mongo_port)
    

# Airport csv headers (not included in the .dat file)
airportHeaders = ['airport_id', 'name', 'city', 'country', 'iata', 'icao',
                  'latitude', 'longitude', 'altitude',
                  'timezone', 'dst', 'tz_type']

# Map that matches header with type
mapHeaderToType = {
    'airport_id': int,
    'name': str,
    'city': str,
    'country': str,
    'iata': str,
    'icao': str,
    'latitude': float,
    'longitude': float,
    'altitude': int,
    'timezone': float,
    'dst': str,
    'tz_type': str
}

# Routes csv headers (not included in the .dat file)
routesHeaders = ['airline', 'airline_id', 'source_airport',
                 'source_airport_id', 'destination_airport',
                 'destination_airport_id', 'code', 'stops', 'equipment']


airports = csv.reader(open("data/airports.dat"), delimiter=',')
routes = csv.reader(open("data/routes.dat"), delimiter=',')
outAirports = open("out/airports.csv", 'w')

db = client['travel-helper']


documents = []
for airport in airports:
    document = {}
    for i in range(0, len(airportHeaders)):
        if airport[i] == '' or airport[i] == '\\N':
            document[airportHeaders[i]] = None
        elif i == 6:
            document['geom'] = {"type": "Point", "coordinates": [
                float(airport[i+1]), float(airport[i])]}
        elif i != 7:
            document[airportHeaders[i]
                     ] = mapHeaderToType[airportHeaders[i]](airport[i])
    documents.append(document)

db.airports.insert_many(documents)

db.airports.create_index([('geom', pymongo.GEOSPHERE)])

db.airports.create_index('airport_id')


documents = []
for route in routes:
    # If the route is a direct flight and the source and destination airport are defined
    if route[7] == '0' and route[3] != '\\N' and route[5] != '\\N':
        source_airport_id = route[3]
        destination_airport_id = route[5]

        source_airport = db.airports.find_one(
            {"airport_id": int(source_airport_id)}, {})
        destination_airport = db.airports.find_one(
            {"airport_id": int(destination_airport_id)}, {})
        #If the source and destination airport aren't defined in our airports database we skip the route
        if source_airport == None or destination_airport == None:
            continue
        doc = {}
        for i in range(0, len(routesHeaders)):
            doc[routesHeaders[i]] = route[i]
        doc['distance'] = list(db.airports.aggregate(([
            {
                "$geoNear": {
                    "near": {
                        "type": "Point",
                        "coordinates": [destination_airport['geom']['coordinates'][0], destination_airport['geom']['coordinates'][1]]
                    },
                    "query": {'airport_id': source_airport['airport_id']},
                    "spherical": True,
                    "distanceField": "distance",
                    "distanceMultiplier": 0.001
                }
            }
        ])))[0]['distance']

        documents.append(doc)

db.routes.insert_many(documents)
