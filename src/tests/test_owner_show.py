from src.routes import OwnerShow
import pytest
from flask import Flask
from flask_restful import Api

@pytest.fixture
def Resource():
    route = OwnerShow()
    return route


@pytest.fixture
def app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(OwnerShow, '/api/owners/<string:id>')

    return app.test_client()


def test_owner_show(app):

    response = app.get("/api/owners/e5a10ee9-0849-4ffb-9a09-9ef179130d3b").json

    assert isinstance(response, list)
    assert len(response) == 1

    assert isinstance(response[0]["full_name"], str)
    assert isinstance(response[0]["address"], str)
    assert isinstance(response[0]["id"], str)
    assert isinstance(response[0]["county_state_zip"], str)
    assert isinstance(response[0]["phone_no"], str)

    assert response[0]["full_name"] == "TRIPLE BOX AB"
    assert response[0]["address"] == "AB VINBARSGATAN 28 BARA, SE SE-233 \t"
    assert response[0]["id"] == "e5a10ee9-0849-4ffb-9a09-9ef179130d3b"
    assert response[0]["county_state_zip"] == "SWEDEN"
    assert response[0]["phone_no"] == "N/A; Lives in Sweden"