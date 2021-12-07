from flask import Flask, request
from flask_restful import Resource, Api
from src.routes import *
import requests
import os
from flask import Flask, render_template

PORT = int(os.environ.get("PORT", 5000))

app = Flask(__name__)
api = Api(app)


api.add_resource(Owners, '/api/owners')
api.add_resource(Units, '/api/units')
api.add_resource(OwnerShow, '/api/owners/<string:id>')
api.add_resource(UnitShow, '/api/units/<string:id>')
api.add_resource(OwnersByUnit, '/api/units/<string:id>/owners')
api.add_resource(CreateOwner, '/api/create_owner')
api.add_resource(CreateUnit, '/api/create_unit')
api.add_resource(CreateUnitOwner, '/api/create_unit_owner')
# api.add_resource(DeleteUnitOwner, '/api/delete_unit_owner')
api.add_resource(DeleteUnitOwner, '/api/units/<string:unit_id>/owners/<string:owner_id>/delete')
api.add_resource(DeleteOwner, '/api/owners/<string:owner_id>/delete')
api.add_resource(PhoneBurnerOwnerShow, '/api/phone_burner/owners/<string:id>')
api.add_resource(EditOwner, '/api/owners/<string:owner_id>/edit')




@app.route("/owners")
def owner_index():
    if "search_params" in request.args:
        data = requests.get("http://localhost:5000/api/owners?search_params={}".format(request.args["search_params"]))
    else:
        data = requests.get("http://localhost:5000/api/owners")

    return render_template("owners/index.html", message=data.json());


@app.route("/units")
def unit_index():
    if "search_params" in request.args:
        data = requests.get("http://localhost:5000/api/units?search_params={}".format(request.args["search_params"]))
    else:
        data = requests.get("http://localhost:5000/api/units")

    return render_template("units/index.html", message=data.json());


@app.route("/owners/<id>/edit", methods=['GET', 'PATCH'])
def owner_edit(id):
    data = requests.get("http://localhost:5000/api/owners/" + str(id))
    if request.method == 'GET':
        return render_template("owners/edit.html", message=data.json());

    else:
        requests.patch("http://localhost:5000/api/owners/{}/edit".format(id))





@app.route("/owners/<id>")
def owner_show(id):
    data = requests.get("http://localhost:5000/api/owners/"+ str(id))
    return render_template("owners/show.html", message=data.json());



@app.route("/units/<id>")
def unit_show(id):
    data = requests.get("http://localhost:5000/api/units/"+ str(id))

    return render_template("units/show.html", message=data.json());


@app.route("/units/<id>/owners")
def unit_owners_index(id):
    data = requests.get("http://localhost:5000/api/units/"+ str(id) +"/owners")

    return render_template("units/owners.html", message=data.json());


@app.route("/")
def welcome_index():
    return render_template("/welcome/index.html");


@app.route("/units/new")
def unit_new():
    return render_template("units/new.html");

@app.route("/owners/new")
def owner_new():
    return render_template("owners/new.html");


@app.route("/units", methods=['POST'])
def unit_create():
    params = request.form.to_dict()
    requests.post("http://localhost:5000/api/create_unit?name={}&legal_description={}&order_no={}".format(params["name"], params["legal_description"], params["order_no"]))
    return render_template("welcome/index.html");

@app.route("/owners", methods=['POST'])
def owner_create():
    params = request.form.to_dict()
    requests.post("http://localhost:5000/api/create_owner?full_name={}&address={}&county_state_zip={}&phone_no={}".format(params["full_name"], params["address"], params["county_state_zip"], params["phone_no"]))
    return render_template("welcome/index.html");

if __name__ == '__main__':
    print("PORT is {}".format(PORT))
    app.run(debug=True,host='0.0.0.0',port=PORT)
