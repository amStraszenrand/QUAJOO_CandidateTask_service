import falcon
from falcon import testing
import msgpack
import pytest
import json

from FalconWebService import api


@pytest.fixture
def client():
    return testing.TestClient(api)


# pytest will inject the object returned by the "client" function
# as an additional parameter.
def test_good_status(client):

    response = client.simulate_get('/temperature')
    assert response.status == falcon.HTTP_OK


def test_listOfCityTemperatures(client):
    filename = "preconfiguredCities"
    filepath = f"../{filename}.json"

    with open(filepath) as file:
        citiesWithTemperatures = json.load(file)

    for city in citiesWithTemperatures:
        response = json.loads(client.simulate_get(f'/temperature?q={city["name"]}').text)
        assert city["id"] == response["id"]