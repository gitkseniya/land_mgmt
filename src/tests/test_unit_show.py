from src.routes import UnitShow
import pytest
from flask import Flask
from flask_restful import Api

@pytest.fixture
def Resource():
    route = UnitShow()
    return route


@pytest.fixture
def app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(UnitShow, "/api/units/<string:id>")

    return app.test_client()


def test_owners_index(app):

    response = app.get("/api/units/bdce98b5-5041-4603-b538-ed39fc9a6ceb").json

    assert isinstance(response, list)
    assert len(response) == 1
    #
    assert isinstance(response[0]["name"], str)
    assert isinstance(response[0]["legal_description"], str)

    assert response[0]["name"] == "Long Creek"
    assert response[0]["legal_description"] == "153N 099W Sec 15,22,23,24,25,26,27,28,33,34 Williams County, ND 6,344 acres"
    assert response[0]["order_no"] is None