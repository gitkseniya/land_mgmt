from flask_restful import Resource, Api
from google.cloud import bigquery
from flask import request

class Owners(Resource):
    def get(self):
        client = bigquery.Client()

        query = """
            SELECT *
            FROM `landmanagementservice.land_deal_info.owners` 
            ORDER BY id
        """

        query_job = client.query(query)

        return [dict(i) for i in query_job]


class Units(Resource):
    def get(self):
        client = bigquery.Client()

        query = """
            SELECT *
            FROM `landmanagementservice.land_deal_info.units` 
        """

        query_job = client.query(query)

        return [dict(i) for i in query_job]


class OwnersByUnit(Resource):
    def get(self, id):
        client = bigquery.Client()

        query = """
            SELECT units_table.name, units_table.legal_description, owners_table.full_name, owners_table.address
             FROM `landmanagementservice.land_deal_info.units` units_table
             
             JOIN `land_deal_info.unit_owners` unit_owners_table
             ON units_table.id = unit_owners_table.unit_id
            
             JOIN `land_deal_info.owners` owners_table
             ON unit_owners_table.owner_id = owners_table.id 
             
             WHERE units_table.id = {}
        """.format(id)

        query_job = client.query(query)

        return [dict(i) for i in query_job]


class CreateOwner(Resource):

    def __init__(self):
        self.args = self._parse_args()

    def _parse_args(self):
        args = {}

        if request.is_json:
            args = request.json
        else:
            args = dict(request.args)

        return args

    def post(self):
        client = bigquery.Client()

        query = """
                    INSERT INTO land_deal_info.owners(full_name, address) 
                    VALUES('{}','{}')
                """.format(self.args["full_name"], self.args["address"])
        # OR: remove args init and .format(request.json["full_name"], request.json["address"])

        query_job = client.query(query)

        print(query_job)
        print(dict(query_job))

        return "owner created"


class CreateUnit(Resource):

    def __init__(self):
        self.args = self._parse_args()

    def _parse_args(self):
        args = {}

        if request.is_json:
            args = request.json
        else:
            args = dict(request.args)

        return args

    def post(self):
        client = bigquery.Client()

        query = """
                    INSERT INTO land_deal_info.units(name, legal_description, order_no) 
                    VALUES('{}','{}', '{}')
                """.format(self.args["name"], self.args["legal_description"], self.args["order_no"])

        query_job = client.query(query)

        return "unit created"


class CreateUnitOwner(Resource):
    def __init__(self):
        self.args = self._parse_args()

    def _parse_args(self):
        args = {}

        if request.is_json:
            args = request.json
        else:
            args = dict(request.args)

        return args

    def post(self):
        client = bigquery.Client()

        query = """
                INSERT INTO land_deal_info.unit_owners(unit_id, owner_id) 
                VALUES({},{})
                """.format(self.args["unit_id"], self.args["owner_id"])

        query_job = client.query(query)

        return "created unit owner"


class DeleteUnitOwner(Resource):
    def __init__(self):
        self.args = self._parse_args()

    def _parse_args(self):
        args = {}

        if request.is_json:
            args = request.json
        else:
            args = dict(request.args)

        return args

    def delete(self):
        client = bigquery.Client()

        query = """
                DELETE land_deal_info.unit_owners
                WHERE unit_id = {} AND owner_id = {}
                """.format(self.args["unit_id"], self.args["owner_id"])

        query_job = client.query(query)

        return "deleted unit owner"