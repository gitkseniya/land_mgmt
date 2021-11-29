from src.routes import Owners
import pytest
from flask import Flask
from flask_restful import Api

@pytest.fixture
def Resource():
    route = Owners()
    return route


@pytest.fixture
def app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Owners, "/api/owners")

    return app.test_client()


def test_owners_index(app):

    response = app.get("/api/owners").json

    assert isinstance(response, list)
    assert len(response) >= 100

    assert isinstance(response[0]["full_name"], str)
    assert isinstance(response[0]["address"], str)
    assert isinstance(response[0]["id"], str)
    assert isinstance(response[0]["county_state_zip"], str)
    assert isinstance(response[0]["phone_no"], str)
