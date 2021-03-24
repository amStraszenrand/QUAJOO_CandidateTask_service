import falcon
import json
import os
import requests
import sys

API_KEY = '4ee98013b7c2a3f89d7d7107b7de04b7'


def getCityTemperature(queryKey, queryValue):
    url = f'http://api.openweathermap.org/data/2.5/weather?{queryKey}={queryValue}&APPID={API_KEY}'

    data = requests.get(url).json()

    if "main" in data.keys():
        temperature = data['main']['temp']
        temperature_celsius = round(temperature - 273.15)

        cityTemperature = {
            "id" : data["id"],
            "name": data["name"],
            "temperature" : temperature_celsius
            }
        status = falcon.HTTP_200

    else:
        cityTemperature = data
        status = falcon.HTTP_404

    return cityTemperature, status


def addCity(response):

    if response.status == falcon.HTTP_200:

        filepath = f"{FalconWebService.foldername}{FalconWebService.filename}.json"
        with open(os.path.join(sys.path[0], filepath)) as file:
            listOfCities = json.load(file)

        if response.media["name"] in [city['name'] for city in listOfCities]:
            response.status = falcon.HTTP_204
        else:
            maxLfdNr = max([city['lfdNr'] for city in listOfCities])
            cityToAdd = {
                    "lfdNr" : maxLfdNr + 1,
                    "id" : response.media["id"],
                    "name": response.media["name"],
                    }

            listOfCities.append(cityToAdd)
            FalconWebService.filename = "extendedCities"
            filepath = f"{FalconWebService.foldername}{FalconWebService.filename}.json"
            with open(os.path.join(sys.path[0], filepath), 'w+', encoding='utf-8') as file:
                json.dump(listOfCities, file, ensure_ascii=False)

            response.status = falcon.HTTP_201


class FalconWebService(object):

    foldername = "./Service/"
    filename = "preconfiguredCities"

    def on_get(self, request, response):

        if "q" in request.params:
            response.media, response.status = getCityTemperature("q", request.params["q"])
        elif "id" in request.params:
            response.media, response.status = getCityTemperature("id", request.params["id"])
        else:
            response.media, response.status = getCityTemperature("q", "Leipzig")


    def on_get_print(self, request, response):

        filepath = f"{FalconWebService.foldername}{FalconWebService.filename}.json"
        with open(os.path.join(sys.path[0], filepath)) as file:
            listOfCities = json.load(file)

        responseMedia = []
        responseStatus = []

        for city in listOfCities:
            responseValues = getCityTemperature("q", city["name"])
            responseMedia.append(responseValues[0])
            responseStatus.append(responseValues[1])

        response.media = responseMedia

        if set(responseStatus) == {falcon.HTTP_200}:
            responseStatusCulminated = falcon.HTTP_200
        elif set(responseStatus) == {falcon.HTTP_204}:
            responseStatusCulminated = falcon.HTTP_204
        else:
            responseStatusCulminated = falcon.HTTP_206
        response.status = responseStatusCulminated


    def on_post_addCityByName(self, request, response):

        response.media, response.status = getCityTemperature("q", request.bounded_stream.read().decode('utf-8'))

        addCity(response)


    def on_post_addCityById(self, request, response):

        response.media, response.status  = getCityTemperature("id", request.bounded_stream.read().decode('utf-8'))

        addCity(response)


class CORSComponent(object):
    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin', 'http://localhost:4200')

        if (req_succeeded
            and req.method == 'OPTIONS'
            and req.get_header('Access-Control-Request-Method')
        ):
            # NOTE(kgriffs): This is a CORS preflight request. Patch the
            #   response accordingly.

            allow = resp.get_header('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_header(
                'Access-Control-Request-Headers',
                default='*'
            )

            resp.set_headers((
                ('Access-Control-Allow-Methods', allow),
                ('Access-Control-Allow-Headers', allow_headers),
                ('Access-Control-Max-Age', '86400'),  # 24 hours
            ))


api = falcon.API(middleware=CORSComponent())

api.add_route('/temperature', FalconWebService())
api.add_route('/temperature/print', FalconWebService(), suffix = 'print')
api.add_route('/temperature/addCityByName', FalconWebService(), suffix = 'addCityByName')
api.add_route('/temperature/addCityById', FalconWebService(), suffix = 'addCityById')