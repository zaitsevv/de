import logging

from sql.writer import AbstractPostgresqlWriter

log = logging.getLogger(__name__)


class StudentService:
    """
    Service class for students table, contains main application methods related to students table
    """

    def __init__(
        self, writer: AbstractPostgresqlWriter, schema: str, students_table: str
    ) -> None:
        self._writer = writer
        self._schema = schema
        self._students_table = students_table

    def write_json_array(self, path: str) -> None:
        """
        Method for writing json array to students table
        :param path: path to the file with data
        :return: None
        """
        with open(path, "r") as file:
            self._writer.bulk_write(self._schema, self._students_table, file.read())
        log.debug(f"Wrote data from {path} to the database")
