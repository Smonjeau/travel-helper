from fastapi import FastAPI
from neo4j import GraphDatabase
import os
app = FastAPI()


neo4j_port = os.environ.get('NEO4J_PORT', 7687)



neo4jClient = GraphDatabase.driver(f"neo4j://192.168.0.246/:{neo4j_port}")

# neo4jClient = GraphDatabase.driver(f"neo4j://localhost:{neo4j_port}")
neo4jSession = neo4jClient.session()






@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/queries/all_routes")
def get_all_routes_between_two_airports(source_airport_code, destination_airport_code):
    #TODO validar datos y tipos de codigos
    max_steps = 1
    result  = neo4jSession.run(
     
        neo_query(max_steps,source_airport_code,destination_airport_code)
     
     )
     # iterate over the result set 
    
    
    values = []
    for ix, record in enumerate(result):
        if ix > 1:
            break
        values.append(record.values())
    info = result.consume()
    print(values,result)
    return {"info":info, "values":values}






@app.get("/queries/all_routes_with_scales")
def get_all_routes_between_two_airports_with_scales(source_airport_code, destination_airport_code,scales):
  result = neo4jSession.run(
     
        neo_query(scales,source_airport_code,destination_airport_code)
     
     )




def neo_query (scales,source,destination):
    return f"MATCH p=(n:Airport {{icao:\"{source}\"}}) -[:HAS_ROUTE_TO*0..{scales}]->(m:Airport{{icao:\"{destination}\"}}) WITH *,relationships(p) as r RETURN n,m,r,nodes(p)"
