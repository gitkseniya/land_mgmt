from flask_restful import Resource, Api
from google.cloud import bigquery
from flask import request
import urllib.request, json

class Owners(Resource):
    def get(self):
        client = bigquery.Client()

        if "search_params" in request.args:
            query = """
                SELECT *
                FROM `landmanagementservice.land_deal_info.owners` 
                WHERE LOWER(full_name) LIKE '%{}%'
            """.format(request.args["search_params"].lower())
        else:
            query = """
                SELECT *
                FROM `landmanagementservice.land_deal_info.owners` 
            """
        print(query)

        query_job = client.query(query)

        return [dict(i) for i in query_job]


class Units(Resource):
    def get(self):
        client = bigquery.Client()

        if "search_params" in request.args:
            query = """
                SELECT *
                FROM `landmanagementservice.land_deal_info.units` 
                WHERE LOWER(name) LIKE '%{search_params}%' 
                OR LOWER(legal_description) LIKE '%{search_params}%' 
                OR LOWER(order_no) LIKE '%{search_params}%' 
            """.format(search_params=request.args["search_params"].lower())
        else:
            query = """
                SELECT *
                FROM `landmanagementservice.land_deal_info.units` 
            """

        query_job = client.query(query)

        return [dict(i) for i in query_job]


class OwnerShow(Resource):
    def get(self, id):
        client = bigquery.Client()

        query = """
            SELECT *
            FROM `landmanagementservice.land_deal_info.owners` 
            WHERE id = '{}'
        """.format(id)

        query_job = client.query(query)

        return [dict(i) for i in query_job]


class UnitShow(Resource):
    def get(self, id):
        client = bigquery.Client()

        query = """
            SELECT *
            FROM `landmanagementservice.land_deal_info.units` 
            WHERE id = '{}'
        """.format(id)

        query_job = client.query(query)

        return [dict(i) for i in query_job]


class OwnersByUnit(Resource):
    def get(self, id):
        client = bigquery.Client()

        query = """
            SELECT units_table.name, units_table.legal_description, owners_table.full_name, owners_table.address, unit_owners_table.interest_type, unit_owners_table.current_owner, unit_owners_table.comments, unit_owners_table.vesting_docs
             FROM `landmanagementservice.land_deal_info.units` units_table
             
             JOIN `land_deal_info.unit_owners` unit_owners_table
             ON units_table.id = unit_owners_table.unit_id
            
             JOIN `land_deal_info.owners` owners_table
             ON unit_owners_table.owner_id = owners_table.id 
             
             WHERE units_table.id = '{}'
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
                    INSERT INTO land_deal_info.owners(id,full_name,address,county_state_zip,phone_no) 
                    VALUES(GENERATE_UUID(),'{}','{}','{}','{}')
                """.format(self.args["full_name"], self.args["address"], self.args["county_state_zip"], self.args["phone_no"])
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
                    INSERT INTO land_deal_info.units(id, name, legal_description, order_no) 
                    VALUES(GENERATE_UUID(),'{}','{}', '{}')
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

    def delete(self, unit_id, owner_id):
        client = bigquery.Client()

        query = """
                DELETE land_deal_info.unit_owners
                WHERE unit_id = {} AND owner_id = {}
                """.format(unit_id, owner_id)

        query_job = client.query(query)

        return "deleted unit owner"


class DeleteOwner(Resource):
    def __init__(self):
        self.args = self._parse_args()

    def _parse_args(self):
        args = {}

        if request.is_json:
            args = request.json
        else:
            args = dict(request.args)

        return args

    def delete(self, owner_id):
        client = bigquery.Client()

        query = """
                DELETE land_deal_info.owners
                WHERE id = '{}'
                """.format(owner_id)

        query_job = client.query(query)

        return "deleted owner"


class DeleteUnit(Resource):
    def __init__(self):
        self.args = self._parse_args()

    def _parse_args(self):
        args = {}

        if request.is_json:
            args = request.json
        else:
            args = dict(request.args)

        return args

    def delete(self, unit_id):
        client = bigquery.Client()

        query = """
                DELETE land_deal_info.units
                WHERE id = '{}'
                """.format(unit_id)

        query_job = client.query(query)

        return "deleted unit"


class PhoneBurnerOwnerShow(Resource):
    def get(self, id):

        # url = "https://www.phoneburner.com/rest/1/contacts?page_size=1&page=1&api_key={}".format(os.environ.get("TMDB_API_KEY"))
        url = "https://api.themoviedb.org/3/movie/76341?api_key=53cee549bb0361b2582b55d6d8ae70fd"

        response = urllib.request.urlopen(url)
        data = response.read()
        dict = json.loads(data)

        return dict


class EditOwner(Resource):
    def __init__(self):
        self.args = self._parse_args()

    def _parse_args(self):
        args = {}

        if request.is_json:
            args = request.json
        else:
            args = dict(request.args)

        return args

    def patch(self, owner_id):
        client = bigquery.Client()

        query = """
                UPDATE landmanagementservice.land_deal_info.owners
                SET full_name = '{}',
                address = '{}',
                county_state_zip = '{}',
                phone_no = '{}'
            
                WHERE id = '{}';
                """.format(self.args['full_name'], self.args['address'], self.args['county_state_zip'], self.args['phone_no'], owner_id)

        query_job = client.query(query)

        return "updated unit owner"

