#!/bin/bash

set -e

pip install pandas

airflow db init

sed -i 's/enable_xcom_pickling = False/enable_xcom_pickling = True/g' "${AIRFLOW_CFG}"
sed -i 's/load_examples = True/load_examples = False/g' "${AIRFLOW_CFG}"

airflow users create \
    --username "${AIRFLOW_USERNAME}" \
    --password "${AIRFLOW_PASSWORD}" \
    --firstname "${AIRFLOW_FIRSTNAME}" \
    --lastname "${AIRFLOW_LASTNAME}" \
    --role "${AIRFLOW_ROLE}" \
    --email "${AIRFLOW_EMAIL}"

airflow webserver --port "${CONTAINER_PORT}" -D
airflow scheduler
