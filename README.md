Get temperatures of cities by their name / id

Dictionary:

cityTemperature = {
    "id" : integer,
    "name": string,
    "temperature" : integer
}

Use Falcon framework in FalconWebService.py

Use class CORSComponent as middleware to allow the Acces-Control-Allow-Origin entrance for the Angular client part

Use 4 routing paths
- /temperature: Get the temperature of Leipzig as default or add parameters ("q", "id") for concrete city search
- /temperature/print: Get the temperature of 10 preconfigured cities (stored in preconfiguredCities.json)
- /temperature/addCityByName: Post a city by its name to save it to the 10 preconfigured cities
- /temperature/addCityById: Post a city by its id to save it to the 10 preconfigured cities
(Before adding the city - check if it is already stored)



