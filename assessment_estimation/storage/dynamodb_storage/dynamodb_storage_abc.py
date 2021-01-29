from abc import ABC, abstractmethod
from typing import Iterator, Any, Dict, List, Optional

import boto3

from assessment_estimation.storage.storages_abc import Storage


class DynamoDBStorage(Storage, ABC):
    dynamodb: object
    table: object

    endpoint_url: str = 'http://localhost:8000'
    table_name: str
    key_schema: List[Dict[str, str]]
    attribute_definitions: List[Dict[str, str]]
    provisioned_throughput: Dict[str, int] = {
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }

    @abstractmethod
    def __init__(self,
                 endpoint_url: Optional[str],
                 provisioned_throughput: Optional[Dict[str, int]]
                 ):
        # provide table name, key_schema, and attribute_definitions here
        pass

    def __setitem__(self, k: str, v: Any) -> None:
        pass

    def __delitem__(self, v: str) -> None:
        pass

    def __getitem__(self, k: str) -> Any:
        pass

    def __len__(self) -> int:
        pass

    def __iter__(self) -> Iterator[Any]:
        pass

    def _connect_to_db(self) -> (object, object):
        if not self.dynamodb:
            self.dynamodb = boto3.resource('dynamodb',
                                           endpoint_url=self.endpoint_url)
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
