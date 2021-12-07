import os
from pymongo import MongoClient
from neo4j import GraphDatabase


if __name__ == "__main__":
    mongo_port = os.environ.get('MONGO_PORT', 27017)
    neo4j_port = os.environ.get('NEO4J_PORT', 7687)

neo4jClient = GraphDatabase.driver(f"neo4j://localhost:{neo4j_port}")
mongoClient = MongoClient(port=mongo_port)
neo4jSession = neo4jClient.session()


mongoDb = mongoClient['travel-helper']
airports = mongoDb.airports.find({})
routes = mongoDb.routes.find({})
for airport in airports:
    neo4jSession.run(
        f"CREATE (a:Airport {{ iata: \"{airport.get('iata','null')}\", icao: \"{airport.get('icao','null')}\", airport_id: {airport['airport_id']} }})")
for route in routes:
    neo4jSession.run(
        f"MATCH (a:Airport {{ airport_id: {route['source_airport_id']}}}), (b:Airport {{ airport_id: {route['destination_airport_id']}}}) CREATE (a)-[r:HAS_ROUTE_TO {{ distance: {route['distance']} }}]->(b)")
