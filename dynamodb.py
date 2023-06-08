import json
import os
import boto3
import decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)

class Dynamodb():

    def __init__(self, table=None):

        self.table = table
        if not self.table:
            self.table = os.getenv('AWS_DYNAMODB_TABLE_MEETINGS')
        self.db_resource = boto3.resource('dynamodb')
        self.db_client = boto3.client('dynamodb')


    def table_list(self, meeting_id=None):

        result = self.db_client.list_tables()

        return result


    def meeting_list(self, meeting_id=None):

        print(self.table)

        table = self.db_resource.Table(self.table)

        # fetch all records from the database
        result = table.scan()

        return result