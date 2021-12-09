from fastapi import HTTPException

max_scales = 2

def validate_airport_codes(source_airport_code, destination_airport_code, airport_code_type):
    if airport_code_type == "IATA":
        if (len(source_airport_code) != 3) or (len(destination_airport_code) != 3):
            raise HTTPException(status_code=400, detail="IATA code must be 3 characters long")
    elif airport_code_type == "ICAO":
        if (len(source_airport_code) != 4) or (len(destination_airport_code) != 4):
            raise HTTPException(status_code=400, detail="ICAO code must be 4 characters long")
    else:
        raise HTTPException(status_code=400, detail="Airport code type must be IATA or ICAO")

def parseResults(results, code_type):
    #TODO Evitar ciclos
    #TODO mostrar tambien informacion de distancia y aerolinea
    code_type = code_type.lower()
    all_results = []
    for result in results:
        new_result = []
        for direct_route in result['r']:
            new_result.append({
                'source': direct_route.nodes[0][code_type],
                'destination': direct_route.nodes[1][code_type],
                'distance': direct_route['distance'],
                'airline_id': direct_route['airline_id'],
            })
        all_results.append(new_result)        
        
    return all_results