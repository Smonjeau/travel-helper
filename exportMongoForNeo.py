import csv
import pymongo
import os

if __name__ == "__main__":
    mongo_port = os.environ.get('MONGO_PORT', 27017)

mongoClient = pymongo.MongoClient(port=mongo_port)
mongoDb = mongoClient['travel-helper']

airports_out = csv.writer(open("data/airports_neo.csv", "w"))
airports_headers = ['iata', 'icao', 'airport_id']
airports_out.writerow(airports_headers)
airports = mongoDb.airports.find({})
for airport in airports:
    airports_out.writerow(['null' if airport['iata'] == None else airport['iata'],
                          'null' if airport['icao'] == None else airport['icao'], airport['airport_id']])

routes_out = csv.writer(open("data/routes_neo.csv", "w"))
routes_headers = ['source_airport_id',
                  'destination_airport_id', 'distance', 'airline_id']
routes_out.writerow(routes_headers)
routes = mongoDb.routes.find({})
for route in routes:
    routes_out.writerow([route['source_airport_id'],
                        route['destination_airport_id'], route['distance'], route['airline_id']])
