#!/bin/bash
#
# Script to simplify the query execution process as postgres user
# Usage: bash run_query.sh <path to file with query>
# Example bash run_query.sh queries/1_categories_with_number_of_films.sql


set -e

ERROR_CONTAINER_NOT_EXIST=1
CONTAINER_NAME='pagila'
USER='postgres'
DB='postgres'
FILE_PATH="${1}"

container_id=$(docker ps | grep "${CONTAINER_NAME}" | cut -d " " -f 1 | head -1)

if [[ -z "${container_id}" ]]; then
  echo "Container <${CONTAINER_NAME}> does not exist"
  exit "${ERROR_CONTAINER_NOT_EXIST}"
fi

query=$(cat "${FILE_PATH}")
docker exec -it --user "${USER}" "${container_id}" psql --username "${USER}" --dbname "${DB}" --command "${query}"
