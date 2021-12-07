def routes_with_scales_support (mins_scales, max_scales, source, destination, code_type):
    scales_multiplier = f"{mins_scales}..{max_scales}" if mins_scales != max_scales else f"{mins_scales}"
    
    from_code_condition = f"icao: \"{source}\"" if code_type == "ICAO" else f"iata: \"{source}\""
    destination_code_condition = f"icao: \"{destination}\"" if code_type == "ICAO" else f"iata: \"{destination}\""

    return f"MATCH p=(n:Airport {{{from_code_condition}}}) -[:HAS_ROUTE_TO*{scales_multiplier}]->(m:Airport{{{destination_code_condition}}}) WITH *,relationships(p) as r RETURN r,nodes(p)"

def airports_reachable_from_airport(source, scales, code_type):
    from_code_condition = f"icao: \"{source}\"" if code_type == "ICAO" else f"iata: \"{source}\""
    return f"MATCH p=(n:Airport {{{from_code_condition}}}) -[:HAS_ROUTE_TO*{scales}]->(m:Airport) WITH *,relationships(p) as r RETURN p,r"

def shorthest_route_between_two_airports(source, destination, code_type):
    from_code_condition = f"icao: \"{source}\"" if code_type == "ICAO" else f"iata: \"{source}\""
    destination_code_condition = f"icao: \"{destination}\"" if code_type == "ICAO" else f"iata: \"{destination}\""

    return f"MATCH p=shortestPath((n:Airport {{{from_code_condition}}})-[:HAS_ROUTE_TO*1..4]-(m:Airport {{{destination_code_condition}}}))RETURN p; "