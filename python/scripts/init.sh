#!/bin/bash
#
# Script to initialize basic entities in the database, executed after initdb call
set -e

psql --username "${POSTGRES_USER}" \
     --dbname "${POSTGRES_DB}" \
     --variable username="${POSTGRES_USER}" \
     --variable hostel_schema="${POSTGRES_HOSTEL_SCHEMA}" \
     --variable rooms_table_full_name="${POSTGRES_ROOMS_TABLE_FULL_NAME}" \
     --variable rooms_table_pk="${POSTGRES_ROOMS_TABLE_PK}" \
     --variable students_table_full_name="${POSTGRES_STUDENTS_TABLE_FULL_NAME}" \
     --variable students_table_pk="${POSTGRES_STUDENTS_TABLE_PK}" \
     --variable students_rooms_id_fk="${POSTGRES_STUDENTS_ROOMS_ID_FK}" \
     --variable students_room_index="${POSTGRES_STUDENTS_ROOM_INDEX}" \
     --file "${DB_SCRIPTS_PATH}/init.sql" \
     --file "${DB_SCRIPTS_PATH}/rooms.sql" \
     --file "${DB_SCRIPTS_PATH}/students.sql"
