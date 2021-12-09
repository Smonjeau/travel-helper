from utils import max_scales


def routes_with_scales_support(mins_scales, _max_scales, source, destination, code_type):
    # _max_scales to avoid the global max_scales variable to be used in the query

    mins_scales += 1
    _max_scales += 1

    scales_multiplier = f"{mins_scales}..{_max_scales}" if mins_scales != _max_scales else f"{mins_scales}"

    from_code_condition = f"icao: \"{source}\"" if code_type == "ICAO" else f"iata: \"{source}\""
    destination_code_condition = f"icao: \"{destination}\"" if code_type == "ICAO" else f"iata: \"{destination}\""

    return f"MATCH p=(n:Airport {{{from_code_condition}}}) -[:HAS_ROUTE_TO*{scales_multiplier}]->(m:Airport{{{destination_code_condition}}}) WITH *, relationships(p) as r WHERE SIZE(apoc.coll.toSet(NODES(p))) > LENGTH(p) RETURN r,nodes(p)"


def airports_reachable(source, scales, code_type):
    scales += 1
    from_code_condition = f"icao: \"{source}\"" if code_type == "ICAO" else f"iata: \"{source}\""
    return f"MATCH p=(n:Airport {{{from_code_condition}}}) -[:HAS_ROUTE_TO*{scales}]->(m:Airport) WITH *,relationships(p) as r WHERE SIZE(apoc.coll.toSet(NODES(p))) > LENGTH(p) RETURN p,r"


def shorthest_route_between_two_airports(source, destination, code_type):
    from_code_condition = f"icao: \"{source}\"" if code_type == "ICAO" else f"iata: \"{source}\""
    destination_code_condition = f"icao: \"{destination}\"" if code_type == "ICAO" else f"iata: \"{destination}\""

    return f"MATCH p=(n:Airport {{{from_code_condition}}})-[r:HAS_ROUTE_TO*1..{max_scales + 1}]->(m:Airport {{{destination_code_condition}}}) WHERE SIZE(apoc.coll.toSet(NODES(p))) > LENGTH(p) RETURN r, nodes(p), reduce(distance=0, r in relationships(p) | distance + toInteger(r.distance)) AS totalDistance ORDER BY totalDistance ASC LIMIT 1;"


def all_routes_between_two_airports_avoiding_airline(source, destination, code_type, airline_code, airline_code_type):
    from_code_condition = f"icao: \"{source}\"" if code_type == "ICAO" else f"iata: \"{source}\" "
    destination_code_condition = f"icao: \"{destination}\"" if code_type == "ICAO" else f"iata: \"{destination}\" "
    airline_code_condition = f"icao = \"{airline_code}\"" if airline_code_type == "ICAO" else f"iata = \"{airline_code}\" "
    return (f"MATCH p=(n:Airport {{{from_code_condition}}})-[r:HAS_ROUTE_TO*1..{max_scales + 1}]->(m:Airport {{{destination_code_condition}}}) "
            "WITH *,relationships(p) as r "
            f"WHERE NOT ANY(route IN r WHERE route.{airline_code_condition}) "
            "AND SIZE(apoc.coll.toSet(NODES(p))) > LENGTH(p) "
            "return p,r")


def all_routes_between_two_airports_avoiding_airport(source, destination, avoid, code_type):
    from_code_condition = f"icao: \"{source}\"" if code_type == "ICAO" else f"iata: \"{source}\" "
    destination_code_condition = f"icao: \"{destination}\"" if code_type == "ICAO" else f"iata: \"{destination}\" "
    avoid_code_condition = f"icao <> \"{avoid}\"" if code_type == "ICAO" else f"iata <> \"{avoid}\" "
    return (f"MATCH p=(n:Airport {{{from_code_condition}}})-[r:HAS_ROUTE_TO*1..{max_scales + 1}]->(m:Airport {{{destination_code_condition}}}) "
            "WITH *,relationships(p) as r "
            f"WHERE ALL(airport IN NODES(p) WHERE airport.{avoid_code_condition}) "
            "AND SIZE(apoc.coll.toSet(NODES(p))) > LENGTH(p) "
            "return p,r")


def airports_with_most_routes(number_of_airports):
    return f"MATCH (a)-[r]->(b)" \
            "RETURN COALESCE(a.iata) as iata, " \
            "count(*) AS outgoing " \
            f"ORDER BY outgoing DESC LIMIT {number_of_airports}"

def most_popular_airports(number_of_airports):
    return f"MATCH (a)<-[r]-(b)" \
            "RETURN COALESCE(a.iata) as iata, " \
            "count(*) AS incoming " \
            f"ORDER BY incoming DESC LIMIT {number_of_airports}"