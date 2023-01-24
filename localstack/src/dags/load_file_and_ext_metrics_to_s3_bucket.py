import os

import pendulum
from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


@dag(schedule='@hourly',
     start_date=pendulum.now(),
     catchup=False)
def load_file_and_ext_metrics_to_s3_bucket() -> None:
    @task
    def load_file(path_to_file: str,
                  bucket_name: str,
                  object_key_prefix: str,
                  s3_hook: S3Hook) -> None:
        s3_hook.load_file(filename=path_to_file,
                          key=f'{object_key_prefix}/{os.path.basename(path_to_file)}',
                          bucket_name=bucket_name)

    path_to_data = Variable.get('PATH_TO_HELSINKI_CITY_BIKES_FILE')
    path_to_spark_tasks_directory = Variable.get('PATH_TO_SPARK_TASKS_DIRECTORY')
    aws_s3_bucket_name = Variable.get('AWS_S3_BUCKET_NAME')
    aws_s3_data_object_key_prefix = Variable.get('AWS_S3_DATA_OBJECT_KEY_PREFIX')
    aws_s3_metrics_object_key_prefix = Variable.get('AWS_S3_METRICS_OBJECT_KEY_PREFIX')

    aws_s3_hook = S3Hook()
    path_to_metrics_file = f'{path_to_data[:-4]}-metrics.csv'

    load_file(path_to_data,
              aws_s3_bucket_name,
              aws_s3_data_object_key_prefix,
              aws_s3_hook)

    spark_submit = SparkSubmitOperator(application=f'{path_to_spark_tasks_directory}/compute_and_save_metrics.py',
                                       task_id='compute_and_save_metrics',
                                       env_vars={'PATH_TO_HELSINKI_CITY_BIKES_FILE': path_to_data,
                                                 'PATH_TO_METRICS_FILE': path_to_metrics_file})
    spark_submit >> load_file.override(task_id='load_metrics_file')(path_to_metrics_file,
                                                                    aws_s3_bucket_name,
                                                                    aws_s3_metrics_object_key_prefix,
                                                                    aws_s3_hook)


load_file_and_ext_metrics_to_s3_bucket()
