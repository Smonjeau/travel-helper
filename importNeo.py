import os
import csv
from neo4j import GraphDatabase


if __name__ == "__main__":
    neo4j_port = os.environ.get('NEO4J_PORT', 7687)

neo4jClient = GraphDatabase.driver(f"neo4j://localhost:{neo4j_port}")
neo4jSession = neo4jClient.session()

print("Importing airports...")
with open('data/airports_neo.csv', 'r') as airports:
    reader =  csv.DictReader(airports)
    transaction = neo4jSession.begin_transaction()
    for airport in reader:
        transaction.run(
        f"CREATE (a:Airport {{ iata: \"{airport.get('iata','null')}\", icao: \"{airport.get('icao','null')}\", airport_id: {airport['airport_id']} }})")
    transaction.commit()
print("Importing routes...")
with open('data/routes_neo.csv', 'r') as routes:
    reader = csv.DictReader(routes)
    transaction = neo4jSession.begin_transaction()
    for route in reader:
        transaction.run(
         f"MATCH (a:Airport {{ airport_id: {route['source_airport_id']}}}), (b:Airport {{ airport_id: {route['destination_airport_id']}}}) CREATE (a)-[r:HAS_ROUTE_TO {{ distance: {route['distance']}, iata: \"{route['iata']}\", icao: \"{route:'icao'}\" }}]->(b)")
    transaction.commit()
