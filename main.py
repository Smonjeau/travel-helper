from fastapi import FastAPI, HTTPException
from neo4j import GraphDatabase
from utils import validate_airport_codes
import os
app = FastAPI()


neo4j_port = os.environ.get('NEO4J_PORT', 7687)

#TODO siempre acordarse de pasar todo a mayuscula o minuscula

neo4jClient = GraphDatabase.driver(f"neo4j://127.0.0.1/:{neo4j_port}")

# neo4jClient = GraphDatabase.driver(f"neo4j://localhost:{neo4j_port}")
neo4jSession = neo4jClient.session()





@app.get("/")
def read_root():
    return {"Hello": "World"}



#query 3
@app.get("/queries/all_routes")
def get_all_routes_between_two_airports(source_airport_code: str, destination_airport_code: str, airport_code_type: str):
    
    validate_airport_codes(source_airport_code, destination_airport_code, airport_code_type)

    max_steps = 1 # TODO ver cual será el max_steps

    result  = neo4jSession.run(
     
        routes_with_scales_support(0, max_steps,source_airport_code,destination_airport_code, airport_code_type)
     
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
def get_all_routes_between_two_airports_with_scales(source_airport_code: str, destination_airport_code: str, airport_code_type: str, scales: int):

    validate_airport_codes(source_airport_code, destination_airport_code, airport_code_type)        
    if(scales > 3):
        raise HTTPException(status_code=400, detail="Scales must be 3 or less")

    results = neo4jSession.run(
        routes_with_scales_support(scales, scales,source_airport_code,destination_airport_code, airport_code_type)
    )
    
    #Iterate over the result set
    for result in results:
        print(result)
    
    

#query 1
@app.get("/queries/shortest_route_in_scales")
def get_shorthest_route_between_two_airports(source_airport_code: str, destination_airport_code: str, airport_code_type: str):

    validate_airport_codes(source_airport_code, destination_airport_code, airport_code_type)

    #TODO usar ICAO o IATA depende el codetype

    result = neo4jSession.run(
     
        f"MATCH p=shortestPath((n:Airport {{icao: \"{source_airport_code}\"}})-[:HAS_ROUTE_TO*1..4]-(m:Airport {{icao: \"{destination_airport_code}\"}}))RETURN p; "
     
     )
    #TODO devolver bien la info
    return result.single()[0]

@app.get("/queries/airports_reachable_from_airport")
def get_airports_reachable_from_airport(source_airport_code: str, airport_code_type: str,scales:int): 

    validate_airport_codes(source_airport_code, source_airport_code, airport_code_type)

    if(scales > 3):
        raise HTTPException(status_code=400, detail="Scales must be 3 or less")
    result = neo4jSession.run(
        f"MATCH p=(n:Airport {{icao:\"{source_airport_code}\"}}) -[:HAS_ROUTE_TO*{scales}]->(m:Airport) WITH *,relationships(p) as r RETURN p"
    )

    #TODO iterar result

def routes_with_scales_support (mins_scales, max_scales, source, destination, code_type):
    scales_multiplier = f"{mins_scales}..{max_scales}" if mins_scales != max_scales else f"{mins_scales}"
    
    from_code_condition = f"icao: \"{source}\"" if code_type == "ICAO" else f"iata: \"{source}\""
    destination_code_condition = f"icao: \"{destination}\"" if code_type == "ICAO" else f"iata: \"{destination}\""

    return f"MATCH p=(n:Airport {{{from_code_condition}}}) -[:HAS_ROUTE_TO*{scales_multiplier}]->(m:Airport{{{destination_code_condition}}}) WITH *,relationships(p) as r RETURN n,m,r,nodes(p)"
