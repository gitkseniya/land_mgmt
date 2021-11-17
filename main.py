from flask import Flask, request
from flask_restful import Resource, Api
from src.routes import *
import requests
import os
from flask import Flask, render_template

app = Flask(__name__)
api = Api(app)



api.add_resource(Owners, '/api/owners')
api.add_resource(Units, '/api/units')
api.add_resource(OwnersByUnit, '/api/units/<int:id>/owners')

@app.route("/owners")
def index():
    data = requests.get("http://localhost:5000/api/owners")

    return render_template("index.html", message=data.json());


if __name__ == '__main__':
    app.run(debug=True)
