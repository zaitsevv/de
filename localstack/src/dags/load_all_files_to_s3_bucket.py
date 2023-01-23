import os

import pendulum
from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


@dag(schedule='@hourly',
     start_date=pendulum.now(),
     catchup=False)
def load_all_files_to_s3_bucket() -> None:
    @task
    def load_all_files(path_to_directory: str,
                       bucket_name: str,
                       object_key_prefix: str,
                       s3_hook: S3Hook) -> None:
        for root, _, files in os.walk(path_to_directory):
            for file in files:
                s3_hook.load_file(filename=os.path.join(root, file),
                                  key=f'{object_key_prefix}/{file}',
                                  bucket_name=bucket_name)

    path_to_data = Variable.get('PATH_TO_HELSINKI_CITY_BIKES_DATA')
    aws_s3_bucket_name = Variable.get('AWS_S3_BUCKET_NAME')
    aws_s3_data_object_key_prefix = Variable.get('AWS_S3_DATA_OBJECT_KEY_PREFIX')

    aws_s3_hook = S3Hook()

    load_all_files(path_to_data,
                   aws_s3_bucket_name,
                   aws_s3_data_object_key_prefix,
                   aws_s3_hook)


load_all_files_to_s3_bucket()
