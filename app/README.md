Get temperatures of cities by their name / id

Dictionary:

cityTemperature = {
    "id" : integer,
    "name": string,
    "temperature" : integer
}

Use Falcon framework in FalconWebService.py with
- on_get: retrieve information from openweathermap for one city
- on_get_print: retrieve information from openweathermap for list of preconfigured cities
- on_post_addCityByName / on_post_addCityByName: add a city to the list of preconfigured cities
(Before adding the city - check if it is already stored)

Therefore use 4 routing paths
- /temperature: Get the temperature of Leipzig as default or add parameters ("q", "id") for concrete city search
- /temperature/print: Get the temperature of 10 preconfigured cities (stored in preconfiguredCities.json)
- /temperature/addCityByName: Post a city by its name to save it to the 10 preconfigured cities
- /temperature/addCityById: Post a city by its id to save it to the 10 preconfigured cities

Use class CORSComponent as middleware to allow the Acces-Control-Allow-Origin entrance for the Angular client part

Home-address is http://localhost:8000

Containing via docker is arranged



