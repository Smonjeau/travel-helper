from fastapi import FastAPI, HTTPException
from neo4j import GraphDatabase
from utils import validate_airport_codes, parseResults
from queries import airports_reachable_from_airport, routes_with_scales_support, shorthest_route_between_two_airports
import os
app = FastAPI()


neo4j_port = os.environ.get('NEO4J_PORT', 7687)

#TODO siempre acordarse de pasar todo a mayuscula o minuscula para comparar
#TODO al comparar code_types pasar a minuscula

neo4jClient = GraphDatabase.driver(f"neo4j://127.0.0.1/:{neo4j_port}")

# neo4jClient = GraphDatabase.driver(f"neo4j://localhost:{neo4j_port}")
neo4jSession = neo4jClient.session()





@app.get("/")
def read_root():
    return {"API Interface": "http://127.0.0.1:8000/docs#/"}



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
    
    return parseResults(results, airport_code_type)
    
    

#query 1
@app.get("/queries/shortest_route_in_scales")
def get_shorthest_route_between_two_airports(source_airport_code: str, destination_airport_code: str, airport_code_type: str):

    validate_airport_codes(source_airport_code, destination_airport_code, airport_code_type)


    results = neo4jSession.run(
        shorthest_route_between_two_airports(source_airport_code, destination_airport_code, airport_code_type)     
     )
    
    return parseResults(results, airport_code_type)

@app.get("/queries/airports_reachable_from_airport")
def get_airports_reachable_from_airport(source_airport_code: str, airport_code_type: str,scales:int): 

    validate_airport_codes(source_airport_code, source_airport_code, airport_code_type)

    if(scales > 3):
        raise HTTPException(status_code=400, detail="Scales must be 3 or less")
    results = neo4jSession.run(
        airports_reachable_from_airport(source_airport_code, airport_code_type,scales)
    )

    return parseResults(results, airport_code_type)


