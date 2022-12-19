from abc import ABC, abstractmethod
from xml.dom.minidom import parseString

import psycopg as pg
import simplejson as json
from dicttoxml import dicttoxml
from psycopg import sql


class AbstractPostgresqlReader(ABC):
    """
    Base class for all classes, that fetches data from Postgresql
    """

    def __init__(self, connection: pg.Connection) -> None:
        self._connection = connection

    @abstractmethod
    def fetch(self, query: sql.Composable) -> str:
        """
        Method for fetching data from Postgresql
        :param query: 'select' query to execute
        :return: result of the query as a string
        """
        pass


class PostgresqlJsonReader(AbstractPostgresqlReader):
    """
    Class that fetches data from Postgresql as json files
    """

    def __init__(self, connection: pg.Connection):
        super().__init__(connection)

    def fetch(self, query: sql.Composable) -> str:
        """
        Method for fetching data from Postgresql as json files
        :param query: 'select' query to execute
        :return: result of the query as a json file
        """
        return json.dumps(self._connection.execute(query).fetchall(), indent=4)


class PostgresqlXmlReader(AbstractPostgresqlReader):
    """
    Class that fetches data from Postgresql as xml files
    """

    INDENT = " " * 4

    def __init__(self, connection: pg.Connection):
        super().__init__(connection)

    def fetch(self, query: sql.Composable) -> str:
        """
        Method for fetching data from Postgresql as xml files
        :param query: 'select' query to execute
        :return: result of the query as a xml file
        """
        result_set = self._connection.execute(query).fetchall()
        xml = dicttoxml(result_set, attr_type=False)
        return parseString(xml).toprettyxml(indent=self.INDENT)
