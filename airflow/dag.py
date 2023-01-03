from datetime import datetime

import pandas as pd
import pymongo as pm
from airflow.decorators import dag, task_group, task
from airflow.models import Variable
from airflow.sensors.filesystem import FileSensor


@dag(schedule=None,
     start_date=datetime.utcnow(),
     catchup=False)
def tiktok_google_play_reviews():
    @task
    def read_csv(path: str) -> pd.DataFrame:
        return pd.read_csv(path)

    @task
    def drop_empty_rows(data: pd.DataFrame) -> pd.DataFrame:
        data.dropna(how='all', inplace=True)
        return data

    @task
    def replace_null_values(data: pd.DataFrame) -> pd.DataFrame:
        data.fillna(value='-', inplace=True)
        return data

    @task
    def sort_by_created_date(data: pd.DataFrame) -> pd.DataFrame:
        data.sort_values(by='at', inplace=True)
        return data

    @task
    def remove_unnecessary_characters_from_content(data: pd.DataFrame) -> pd.DataFrame:
        data['content'].replace(to_replace=r'[^\w\s.,?!:\'\(\)\-]', value='', regex=True, inplace=True)
        return data

    @task
    def load_to_mongodb(data: pd.DataFrame,
                        host: str,
                        port: str,
                        username: str,
                        password: str,
                        db_name: str,
                        collection_name: str) -> None:
        connection_str = f'mongodb://{username}:{password}@{host}:{port}'
        client = pm.MongoClient(connection_str)
        db = client[db_name]
        collection = db[collection_name]
        collection.insert_many(data.to_dict(orient='records'))

    @task_group
    def process_data(data: pd.DataFrame) -> pd.DataFrame:
        return remove_unnecessary_characters_from_content(
            sort_by_created_date(
                replace_null_values(
                    drop_empty_rows(data))))

    path_to_data = Variable.get('PATH_TO_DATA')
    mongodb_host = Variable.get('MONGODB_HOST')
    mongodb_port = Variable.get('MONGODB_PORT')
    mongodb_username = Variable.get('MONGODB_USERNAME')
    mongodb_password = Variable.get('MONGODB_PASSWORD')
    mongodb_db_name = Variable.get('MONGODB_DB_NAME')
    mongodb_collection_name = Variable.get('MONGODB_COLLECTION_NAME')

    wait_for_data = FileSensor(task_id='wait_for_data',
                               poke_interval=1,
                               filepath=path_to_data)

    csv_data = wait_for_data >> read_csv(path_to_data)
    load_to_mongodb(process_data(csv_data),
                    mongodb_host,
                    mongodb_port,
                    mongodb_username,
                    mongodb_password,
                    mongodb_db_name,
                    mongodb_collection_name)


tiktok_google_play_reviews()
