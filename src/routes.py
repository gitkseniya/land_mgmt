from flask_restful import Resource, Api
from google.cloud import bigquery


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
    def post(self):
        client = bigquery.Client()

        query = """
            SELECT *
            FROM `landmanagementservice.land_deal_info.owners` 
            ORDER BY id
        """

        query_job = client.query(query)

        return [dict(i) for i in query_job]