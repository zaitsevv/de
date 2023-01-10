from datetime import datetime

import pandas as pd
from airflow.decorators import dag, task
from airflow.models import Variable
from snowflake.connector import SnowflakeConnection
from snowflake.connector import connect as snowflake_connect
from snowflake.connector.cursor import SnowflakeCursor
from snowflake.connector.pandas_tools import write_pandas


@dag(schedule=None,
     start_date=datetime.utcnow(),
     catchup=False)
def create_data_streams_and_load_csv():
    @task
    def read_csv(path: str) -> pd.DataFrame:
        dataframe = pd.read_csv(path, index_col=False)
        dataframe.columns = dataframe.columns.str.upper()
        return dataframe

    @task
    def create_raw_stream(stream_name: str,
                          table_name: str,
                          cursor: SnowflakeCursor) -> None:
        cursor.execute(f'CREATE STREAM IF NOT EXISTS {stream_name} ON TABLE {table_name}')

    @task
    def create_stage_stream(stream_name: str,
                            table_name: str,
                            cursor: SnowflakeCursor) -> None:
        cursor.execute(f'CREATE STREAM IF NOT EXISTS {stream_name} ON TABLE {table_name}')

    @task
    def insert_into_raw_table(dataframe: pd.DataFrame,
                              table_name: str,
                              connection: SnowflakeConnection) -> None:
        write_pandas(connection, dataframe, table_name)

    @task
    def insert_into_stage_table(raw_table_name: str,
                                stage_table_name: str,
                                cursor: SnowflakeCursor) -> None:
        cursor.execute(f'INSERT INTO {stage_table_name} SELECT * FROM {raw_table_name}')

    @task
    def insert_into_master_table(stage_table_name: str,
                                 master_table_name: str,
                                 cursor: SnowflakeCursor) -> None:
        cursor.execute(f'INSERT INTO {master_table_name} SELECT * FROM {stage_table_name}')

    snowflake_user = Variable.get('SNOWFLAKE_USER')
    snowflake_password = Variable.get('SNOWFLAKE_PASSWORD')
    snowflake_account = Variable.get('SNOWFLAKE_ACCOUNT')
    snowflake_warehouse = Variable.get('SNOWFLAKE_WAREHOUSE')
    snowflake_database = Variable.get('SNOWFLAKE_DATABASE')
    snowflake_schema = Variable.get('SNOWFLAKE_SCHEMA')
    path_to_data = Variable.get('PATH_TO_DATA')
    raw_stream_name = Variable.get('RAW_STREAM_NAME')
    stage_stream_name = Variable.get('STAGE_STREAM_NAME')
    raw_table_name = Variable.get('RAW_TABLE_NAME')
    stage_table_name = Variable.get('STAGE_TABLE_NAME')
    master_table_name = Variable.get('MASTER_TABLE_NAME')

    connection = snowflake_connect(user=snowflake_user,
                                   password=snowflake_password,
                                   account=snowflake_account,
                                   warehouse=snowflake_warehouse,
                                   database=snowflake_database,
                                   schema=snowflake_schema)

    dataframe = read_csv(path_to_data)
    [create_raw_stream(raw_stream_name, stage_table_name, connection.cursor()),
     dataframe] >> \
        insert_into_raw_table(dataframe, raw_table_name, connection) >> \
        (create_stage_stream(stage_stream_name, master_table_name, connection.cursor()) >>
            insert_into_stage_table(raw_table_name, stage_table_name, connection.cursor())) >> \
        insert_into_master_table(stage_table_name, master_table_name, connection.cursor())


create_data_streams_and_load_csv()
