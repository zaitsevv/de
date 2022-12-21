import logging

from psycopg import sql

from sql import queries as sq
from sql.reader import (
    AbstractPostgresqlReader,
    PostgresqlJsonReader,
    PostgresqlXmlReader,
)
from sql.writer import AbstractPostgresqlWriter

log = logging.getLogger(__name__)


class RoomService:
    """
    Service class for rooms table, contains main application methods related to rooms table
    """

    ROOMS_WITH_NUMBER_OF_STUDENTS_FILE = "rooms_with_number_of_students"
    ROOMS_WITH_FIVE_min_AVG_STUDENTS_AGES_FILE = "rooms_with_five_min_avg_students_ages"
    ROOMS_WITH_FIVE_MAX_STUDENTS_AGE_DIFF_FILE = "rooms_with_five_max_students_age_diff"
    ROOMS_WITH_DIFFERENT_STUDENTS_GENDER = "rooms_with_different_student_gender"

    def __init__(
        self,
        writer: AbstractPostgresqlWriter,
        reader: AbstractPostgresqlReader,
        schema: str,
        rooms_table: str,
        students_table: str,
    ) -> None:
        self._writer = writer
        self._reader = reader
        self._schema = schema
        self._rooms_table = rooms_table
        self._students_table = students_table
        self._file_format = (
            "json"
            if isinstance(reader, PostgresqlJsonReader)
            else "xml"
            if isinstance(reader, PostgresqlXmlReader)
            else "unknown"
        )

    def fetch_rooms_with_number_of_students(self, path: str) -> None:
        """
        Method for fetch data from database, see :func:`__fetch_data_template`
        :param path: path for output file directory
        :return: None
        """
        self.__fetch_data_template(
            path,
            self.ROOMS_WITH_NUMBER_OF_STUDENTS_FILE,
            sq.FETCH["rooms_with_number_of_students"],
        )

    def fetch_rooms_with_five_min_avg_students_ages(self, path: str) -> None:
        """
        Method for fetch data from database, see :func:`__fetch_data_template`
        :param path: path for output file directory
        :return: None
        """
        self.__fetch_data_template(
            path,
            self.ROOMS_WITH_FIVE_min_AVG_STUDENTS_AGES_FILE,
            sq.FETCH["rooms_with_five_min_avg_students_ages"],
        )

    def fetch_rooms_with_five_max_students_age_diff(self, path: str) -> None:
        """
        Method for fetch data from database, see :func:`__fetch_data_template`
        :param path: path for output file directory
        :return: None
        """
        self.__fetch_data_template(
            path,
            self.ROOMS_WITH_FIVE_MAX_STUDENTS_AGE_DIFF_FILE,
            sq.FETCH["rooms_with_five_max_students_age_diff"],
        )

    def fetch_rooms_with_different_students_gender(self, path: str) -> None:
        """
        Method for fetch data from database, see :func:`__fetch_data_template`
        :param path: path for output file directory
        :return: None
        """
        self.__fetch_data_template(
            path,
            self.ROOMS_WITH_DIFFERENT_STUDENTS_GENDER,
            sq.FETCH["rooms_with_different_students_gender"],
        )

    def write_json_array(self, path: str) -> None:
        """
        Method for writing json array to rooms table
        :param path: path to the file with data
        :return: None
        """
        with open(path, "r") as file:
            self._writer.bulk_write(self._schema, self._rooms_table, file.read())
        log.debug(f"Wrote data from {path} to the database")

    def __fetch_data_template(self, path: str, file_name: str, query: str) -> None:
        """
        Template for all 'fetch' methods, execute passed query and write result to a json/xml file
        :param path: path to the file with data
        :param file_name: name of the result file
        :param query: query to execute
        :return: None
        """
        full_file_path = f"{path}/{file_name}.{self._file_format}"
        with open(full_file_path, "w") as file:
            content = self._reader.fetch(
                sql.SQL(query).format(
                    schema=sql.Identifier(self._schema),
                    rooms_table=sql.Identifier(self._rooms_table),
                    students_table=sql.Identifier(self._students_table),
                )
            )
            file.write(content)
        log.debug(f"Wrote data from database to {full_file_path}")
