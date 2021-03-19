from typing import Iterable

from sqlitedict import SqliteDict

from assessment_estimation.models.models import Group, Task, TopicSet
from assessment_estimation.storage.storages_abc import StudentStorage, \
    GroupStorage, AssessmentStorage, TaskStorage, TopicSetsStorage


class SQLiteDictStudentStorage(StudentStorage, SqliteDict):
    pass


class SQLiteDictGroupStorage(GroupStorage, SqliteDict):
    def get_by_year(self, year: int) -> Iterable[Group]:
        pass

    def get_by_speciality(self, speciality_name: str) -> Iterable[Group]:
        pass


class SQLiteDictAssessmentStorage(AssessmentStorage, SqliteDict):
    pass


class SQLiteDictTaskStorage(TaskStorage, SqliteDict):
    def get_by_topic(self, topic_name: str) -> Iterable[Task]:
        pass

    def get_topic_names(self, topic_name: str) -> Iterable[str]:
        pass


class SQLiteDictTopicSetsStorage(TopicSetsStorage, SqliteDict):
    def get_by_topic_uid_in(self, topic_uid: str) -> Iterable[TopicSet]:
        pass
