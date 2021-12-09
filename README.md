# Travel-Helper

## Considerations
- Airport codes can be [IATA](https://www.nationsonline.org/oneworld/IATA_Codes/airport_code_list.htm) or [ICAO](https://en.wikipedia.org/wiki/List_of_airports_by_ICAO_code:_A).
- The maximum number of scales is 2. (Can be modified from the code)

## Set up

Pull docker images

```bash
docker pull fquesada00/travel-helper-mongo
```
```bash
docker pull fquesada00/travel-helper-neo
```

Create the mongo container
```bash
docker run --name travel-helper-mongo -p 27017:27017 -d fquesada/travel-helper-mongo
```
Create the neo4j container (might take about 10 minutes)


In Linux
```bash
docker run --name travel-helper-neo -p 7474:7474 -p 7687:7687 --env=NEO4J_AUTH=none --env NEO4JLABS_PLUGINS='["apoc"]' -d fquesada00/travel-helper-neo
```

In Windows
```bash
docker run --name travel-helper-neo -p 7474:7474 -p 7687:7687 --env NEO4J_AUTH=none --env NEO4JLABS_PLUGINS="[\"apoc\"]" --rm -d fquesada00/travel-helper-neo
```


## Turn on the server
Python 3.X is required.

Install dependencies
```bash
pip install -r requirements.txt
```

Run the server
```bash
uvicorn main:app --reload
```

## Front-end
It's located at <server_url>/front
