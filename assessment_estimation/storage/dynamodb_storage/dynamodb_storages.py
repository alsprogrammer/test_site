from assessment_estimation.storage.dynamodb_storage.dynamodb_storage_abc import \
    DynamoDBStorage
from assessment_estimation.storage.storages_abc import AssessmentStorage, \
    StudentStorage, GroupStorage, TaskStorage, TopicSetsStorage


class InMemoryAssessmentStorage(DynamoDBStorage, AssessmentStorage):
    pass


class InMemoryStudentStorage(DynamoDBStorage, StudentStorage):
    pass


class InMemoryGroupStorage(DynamoDBStorage, GroupStorage):
    pass


class InMemoryTaskStorage(DynamoDBStorage, TaskStorage):
    pass


class InMemoryTopicSetsStorage(DynamoDBStorage, TopicSetsStorage):
    pass
