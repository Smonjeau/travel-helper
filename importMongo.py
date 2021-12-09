import csv
import os
import pymongo
if __name__ == "__main__":
    mongo_port = os.environ.get('MONGO_PORT', 27017)
    neo4j_port = os.environ.get('NEO4J_PORT', 7687)

mongoClient = pymongo.MongoClient(port=mongo_port)


# Airport csv headers (not included in the .dat file)
airportHeaders = ['airport_id', 'name', 'city', 'country', 'iata', 'icao',
                  'latitude', 'longitude', 'altitude',
                  'timezone', 'dst', 'tz_type']

# Map that matches header with type
mapAirportHeaderToType = {
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

countriesHeaders = ['name', 'iso_code', 'dafif_code']

airlinesHeaders = ['airline_id', 'name', 'alias',
                   'iata', 'icao', 'callsign', 'country', 'active']
mapAirlineHeaderToType = {
    'airline_id': int,
    'name': str,
    'alias': str,
    'iata': str,
    'icao': str,
    'callsign': str,
    'country': str,
    'active': str,
}

airports = csv.reader(open("data/airports.dat"), delimiter=',')
routes = csv.reader(open("data/routes.dat"), delimiter=',')
countries = csv.reader(open("data/countries.dat"), delimiter=',')
airlines = csv.reader(open("data/airlines.dat"), delimiter=',')


mongoDb = mongoClient['travel-helper']


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
                     ] = mapAirportHeaderToType[airportHeaders[i]](airport[i])
    documents.append(document)

mongoDb.airports.insert_many(documents)

mongoDb.airports.create_index([('geom', pymongo.GEOSPHERE)])

mongoDb.airports.create_index('airport_id')

documents = []
for country in countries:
    document = {}
    if country[1] != '\\N':
        for i in range(0, len(countriesHeaders)):
            document[countriesHeaders[i]] = country[i]
        documents.append(document)
mongoDb.countries.insert_many(documents)


documents = []
for airline in airlines:
    doc = {}
    i = 0
    for header in airlinesHeaders:

        if airline[i] == '\\N':
            doc[header] = None
        else:
            doc[header] = mapAirlineHeaderToType[header](airline[i])
        i += 1
    documents.append(doc)
mongoDb.airlines.insert_many(documents)
mongoDb.airlines.create_index('airline_id')



documents = []
for route in routes:
    # If the route is a direct flight and the source and destination airport are defined and route has associated airline
    if route[7] == '0' and route[3] != '\\N' and route[5] != '\\N' and route[1] != '\\N':
        source_airport_id = route[3]
        destination_airport_id = route[5]

        source_airport = mongoDb.airports.find_one(
            {"airport_id": int(source_airport_id)}, {})
        destination_airport = mongoDb.airports.find_one(
            {"airport_id": int(destination_airport_id)}, {})
        # If the source and destination airport aren't defined in our airports database we skip the route
        if source_airport == None or destination_airport == None:
            continue
        doc = {}
        for i in range(0, len(routesHeaders)):
            doc[routesHeaders[i]] = route[i]
        doc['distance'] = list(mongoDb.airports.aggregate(([
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
        airline = mongoDb.airlines.find_one({"airline_id": int(doc['airline_id'])}, {})
        doc['icao'] = airline['icao']
        doc['iata'] = airline['iata']

        documents.append(doc)

mongoDb.routes.insert_many(documents)
mongoDb.routes.create_index('source_airport_id')
mongoDb.routes.create_index('destination_airport_id')
mongoDb.routes.create_index('airline_id')
mongoDb.routes.create_index('icao')
mongoDb.routes.create_index('iata')
