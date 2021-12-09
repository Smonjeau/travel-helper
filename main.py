from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from neo4j import GraphDatabase
import pymongo
from utils import parseTopAirports, validate_airline_code, validate_airport_codes, parseResults, max_scales
from queries import airports_reachable, airports_with_most_routes, all_routes_between_two_airports_avoiding_airline, all_routes_between_two_airports_avoiding_airport, most_popular_airports, routes_with_scales_support, shorthest_route_between_two_airports
import os
app = FastAPI()

app.mount("/front", StaticFiles(directory="front", html=True), name="static")


neo4j_port = os.environ.get('NEO4J_PORT', 7687)
mongo_port = os.environ.get('MONGO_PORT', 27017)

# TODO siempre acordarse de pasar todo a mayuscula o minuscula para comparar
# TODO al comparar code_types pasar a minuscula
# TODO manejar bien posibles errores (neo principalmente)


#neo4jClient = GraphDatabase.driver(f"neo4j://192.168.0.246/:{neo4j_port}")

neo4jClient = GraphDatabase.driver(f"neo4j://127.0.0.1/:{neo4j_port}")
mongoClient = pymongo.MongoClient(port=mongo_port)

mongoDB = mongoClient['travel-helper']

# neo4jClient = GraphDatabase.driver(f"neo4j://localhost:{neo4j_port}")


@app.get("/")
def read_root():
    return {"API Interface": "http://127.0.0.1:8000/docs#/"}


# query 3
@app.get("/queries/all_routes")
def get_all_routes_between_two_airports(source_airport_code: str, destination_airport_code: str, airport_code_type: str):

    validate_airport_codes(airport_code_type, source_airport_code,
                           destination_airport_code)

    try:
        neo4jSession = neo4jClient.session()
        result = neo4jSession.run(
            routes_with_scales_support(0, max_scales, source_airport_code.upper(
            ), destination_airport_code.upper(), airport_code_type)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return parseResults(result, airport_code_type, mongoDB)


@app.get("/queries/all_routes_with_scales")
def get_all_routes_between_two_airports_with_scales(source_airport_code: str, destination_airport_code: str, airport_code_type: str, scales: int):

    validate_airport_codes(airport_code_type, source_airport_code,
                           destination_airport_code)
    if(scales > 3 or scales < 0):
        raise HTTPException(status_code=400, detail="Scales must be 3 or less")

    try:
        neo4jSession = neo4jClient.session()
        results = neo4jSession.run(
            routes_with_scales_support(scales, scales, source_airport_code.upper(
            ), destination_airport_code.upper(), airport_code_type)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return parseResults(results, airport_code_type, mongoDB)


# query 1
@app.get("/queries/shortest_route_in_scales")
def get_shorthest_route_between_two_airports(source_airport_code: str, destination_airport_code: str, airport_code_type: str):

    validate_airport_codes(airport_code_type, source_airport_code,
                           destination_airport_code)

    try:
        neo4jSession = neo4jClient.session()
        results = neo4jSession.run(
            shorthest_route_between_two_airports(source_airport_code.upper(
            ), destination_airport_code.upper(), airport_code_type)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return parseResults(results, airport_code_type, mongoDB)


@app.get("/queries/airports_reachable_from_airport")
def get_airports_reachable_from_airport(source_airport_code: str, airport_code_type: str, scales: int):

    validate_airport_codes(airport_code_type, source_airport_code,
                           source_airport_code)

    if(scales < 0):
        raise HTTPException(
            status_code=400, detail="Scales must be at least 0")

    try:
        neo4jSession = neo4jClient.session()
        results = neo4jSession.run(
            airports_reachable(source_airport_code.upper(),
                               scales, airport_code_type)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return parseResults(results, airport_code_type, mongoDB)


@app.get("/queries/all_routes_avoiding_airline")
def get_all_routes_between_two_airports_avoiding_airline(source_airport_code: str, destination_airport_code: str, airport_code_type: str, airline_code: str, airline_code_type: str):

    validate_airport_codes(airport_code_type, source_airport_code,
                           destination_airport_code)
    validate_airline_code(airline_code, airline_code_type)
    try:
        neo4jSession = neo4jClient.session()
        results = neo4jSession.run(
            all_routes_between_two_airports_avoiding_airline(source_airport_code.upper(),
                                                             destination_airport_code.upper(),
                                                             airport_code_type,
                                                             airline_code.upper(), airline_code_type)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return parseResults(results, airport_code_type, mongoDB)


@app.get("/queries/all_routes_avoiding_airport")
def get_all_routes_between_two_airports_avoiding_airport(source_airport_code: str, destination_airport_code: str, airport_code_type: str, airport_code: str):

    validate_airport_codes(airport_code_type, source_airport_code,
                           destination_airport_code)
    try:
        neo4jSession = neo4jClient.session()
        results = neo4jSession.run(
            all_routes_between_two_airports_avoiding_airport(source_airport_code.upper(),
                                                             destination_airport_code.upper(),
                                                             airport_code.upper(),
                                                             airport_code_type)

        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return parseResults(results, airport_code_type, mongoDB)


@app.get("/queries/airports_with_most_routes")
def get_airports_with_most_routes( number_of_airports: int):
    
        if(number_of_airports < 0):
            raise HTTPException(
                status_code=400, detail="Number of airports must be at least 0")
    
        try:
            neo4jSession = neo4jClient.session()
            results = neo4jSession.run(
                airports_with_most_routes(number_of_airports)
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        return parseTopAirports(results, mongoDB,"outgoing")

@app.get("/queries/most_popular_airports")
def get_airports_with_most_routes( number_of_airports: int):
    
        if(number_of_airports < 0):
            raise HTTPException(
                status_code=400, detail="Number of airports must be at least 0")
    
        try:
            neo4jSession = neo4jClient.session()
            results = neo4jSession.run(
                most_popular_airports(number_of_airports)
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        return parseTopAirports(results, mongoDB,"incoming")

