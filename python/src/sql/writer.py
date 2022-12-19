from abc import ABC, abstractmethod

import psycopg as pg
from psycopg import sql

from sql import queries as sq


class AbstractPostgresqlWriter(ABC):
    """
    Base class for all classes, that write data to Postgresql
    """

    def __init__(self, connection: pg.Connection) -> None:
        self._connection = connection

    @abstractmethod
    def bulk_write(self, schema: str, table: str, data: str) -> None:
        """
        Method for writing array of data to Postgresql
        :param schema: schema name
        :param table: table name
        :param data: data to write
        :return: None
        """
        pass


class PostgresqlJsonWriter(AbstractPostgresqlWriter):
    """
    Class that writes json files to Postgresql
    """

    def __init__(self, connection: pg.Connection):
        super().__init__(connection)

    def bulk_write(self, schema: str, table: str, data: str) -> None:
        """
        Method for writing json array to Postgresql
        :param schema: schema name
        :param table: table name
        :param data: json array as a string
        :return: None
        """
        with self._connection.execute(
            sql.SQL(sq.INSERT["json_array"]).format(
                schema=sql.Identifier(schema),
                table=sql.Identifier(table),
                json=sql.Literal(data),
            )
        ):
            pass
