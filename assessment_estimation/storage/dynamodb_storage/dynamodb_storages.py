from assessment_estimation.storage.dynamodb_storage.dynamodb_storage_abc import \
    DynamoDBStorage
from assessment_estimation.storage.storages_abc import AssessmentStorage, \
    StudentStorage, GroupStorage, TaskStorage, TopicSetsStorage


class DynamoDBAssessmentStorage(DynamoDBStorage, AssessmentStorage):
    pass


class DynamoDBStudentStorage(DynamoDBStorage, StudentStorage):
    pass


class DynamoDBGroupStorage(DynamoDBStorage, GroupStorage):
    pass


class DynamoDBTaskStorage(DynamoDBStorage, TaskStorage):
    pass


class DynamoDBTopicSetsStorage(DynamoDBStorage, TopicSetsStorage):
    pass
