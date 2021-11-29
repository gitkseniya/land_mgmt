from src.routes import Units
import pytest
from flask import Flask
from flask_restful import Api

@pytest.fixture
def Resource():
    route = Units()
    return route


@pytest.fixture
def app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Units, "/api/units")

    return app.test_client()


def test_owners_index(app):

    response = app.get("/api/units").json

    assert isinstance(response, list)
    assert len(response) >= 3

    assert isinstance(response[0]["name"], str)
    assert isinstance(response[0]["legal_description"], str)
    # assert isinstance(response[0]["order_no"], str)
