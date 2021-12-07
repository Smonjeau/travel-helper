from fastapi import HTTPException

def validate_airport_codes(source_airport_code, destination_airport_code, airport_code_type):
    if airport_code_type == "IATA":
        if (len(source_airport_code) != 3) or (len(destination_airport_code) != 3):
            raise HTTPException(status_code=400, detail="IATA code must be 3 characters long")
    elif airport_code_type == "ICAO":
        if (len(source_airport_code) != 4) or (len(destination_airport_code) != 4):
            raise HTTPException(status_code=400, detail="ICAO code must be 4 characters long")
    else:
        raise HTTPException(status_code=400, detail="Airport code type must be IATA or ICAO")