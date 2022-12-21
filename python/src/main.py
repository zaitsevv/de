import logging.config
import os

import click as cl
import psycopg as pg
from psycopg.rows import dict_row

from service import RoomService, StudentService
from sql.reader import PostgresqlJsonReader, PostgresqlXmlReader
from sql.writer import PostgresqlJsonWriter

logging.config.fileConfig(fname="configs/log.conf")
log = logging.getLogger(__name__)


@cl.command
@cl.option(
    "-r", "--rooms-path", help="Path to file with data about rooms", type=cl.STRING
)
@cl.option(
    "-s",
    "--students-path",
    help="Path to file with data about students",
    type=cl.STRING,
)
@cl.option("-o", "--output-path", type=cl.STRING, help="Output file path")
@cl.option(
    "-f",
    "--output-format",
    help="Output file format",
    type=cl.Choice(["json", "xml"]),
)
def main(
    rooms_path: str, students_path: str, output_path: str, output_format: str
) -> None:
    """
    The function with main logic of the application, creates and injects dependencies for the service class, after runs
    all necessary 'fetch' methods.
    :param rooms_path: path to a file with data about rooms
    :param students_path: path to a file with data about students
    :param output_path: path to files with results of the select queries
    :param output_format: result files format, json or xml
    :return: None
    """
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("HOST_PORT")
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    schema = os.getenv("POSTGRES_HOSTEL_SCHEMA")
    rooms = os.getenv("POSTGRES_ROOMS_TABLE")
    students = os.getenv("POSTGRES_STUDENTS_TABLE")
    log.info("Creating a connection to Postgresql...")
    connection = pg.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
        row_factory=dict_row,
        autocommit=True,
    )
    log.info("Successfully!")
    writer = PostgresqlJsonWriter(connection)
    reader = (
        PostgresqlJsonReader(connection)
        if output_format == "json"
        else PostgresqlXmlReader(connection)
    )
    room_service = RoomService(writer, reader, schema, rooms, students)
    student_service = StudentService(writer, schema, students)
    log.info("Writing data to hostel.rooms table...")
    room_service.write_json_array(rooms_path)
    log.info("Successfully!")
    log.info("Writing data to hostel.students table...")
    student_service.write_json_array(students_path)
    log.info("Successfully!")
    log.info(f"Creating {output_format} files with result of the select queries...")
    room_service.fetch_rooms_with_number_of_students(output_path)
    room_service.fetch_rooms_with_five_min_avg_students_ages(output_path)
    room_service.fetch_rooms_with_five_max_students_age_diff(output_path)
    room_service.fetch_rooms_with_different_students_gender(output_path)
    log.info("Successfully!")


if __name__ == "__main__":
    main()
