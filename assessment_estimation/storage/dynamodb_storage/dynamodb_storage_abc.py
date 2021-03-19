from abc import ABC
from typing import Iterator, Any, Dict, List, Optional

import boto3
from botocore.exceptions import ClientError

from assessment_estimation.models.models import Model
from assessment_estimation.storage.storages_abc import Storage


class DynamoDBStorage(Storage, ABC):
    dynamodb: boto3.resources.factory.dynamodb.ServiceResource
    table: boto3.resources.factory.dynamodb.Table

    region: str
    endpoint_url: str = 'http://localhost:8000'
    table_name: str
    key_schema: List[Dict[str, str]]
    attribute_definitions: List[Dict[str, str]]
    provisioned_throughput: Dict[str, int] = {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }

    def __init__(self,
                 table_name: str,
                 endpoint_url: Optional[str],
                 region: str,
                 provisioned_throughput: Optional[Dict[str, int]] = None
                 ):
        # provide table name, key_schema, and attribute_definitions here
        self.table_name = table_name
        self.endpoint_url = endpoint_url
        self.region = region
        self.provisioned_throughput = provisioned_throughput or {
                     'ReadCapacityUnits': 10,
                     'WriteCapacityUnits': 10
                 }
        self._connect_to_db()

    def __setitem__(self, k: str, v: Model) -> None:
        v.uuid = k
        self.table.put_item(Item=v)

    def __delitem__(self, v: Model) -> None:
        try:
            response = self.table.delete_item(
                Key={
                    'uuid': v.uuid,
                },
            )
        except ClientError as e:
            if e.response['Error']['Code'] == "ConditionalCheckFailedException":
                print(e.response['Error']['Message'])
            else:
                raise
        else:
            return response

    def __getitem__(self, k: str) -> Model:
        try:
            response = self.table.get_item(Key={'uuid': k})
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']

    def __len__(self) -> int:
        return self.table.item_countS

    def __iter__(self) -> Iterator[Any]:
        raise ValueError("You should never, NEVER iterate through the whole "
                         "storage")

    def _connect_to_db(self) -> (object, object):
        if not self.dynamodb:
            self.dynamodb = boto3.resource('dynamodb',
                                           endpoint_url=self.endpoint_url,
                                           region=self.region)
        self.table = self.dynamodb.Table(self.table_name)
        if not self.table:
            self.table = self._create_table_if_not_exists()

    def _create_table_if_not_exists(self) -> object:
        table = self.dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=self.key_schema,
            AttributeDefinitions=self.attribute_definitions,
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        return table
