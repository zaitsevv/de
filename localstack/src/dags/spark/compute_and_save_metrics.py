import os

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def compute_metrics(path_to_file: str,
                    session: SparkSession) -> DataFrame:
    df = session.read \
        .option('header', True) \
        .csv(path_to_file)
    departure_count_df = df \
        .groupby('departure_name') \
        .count() \
        .select(col('departure_name').alias('station_name'),
                col('count').alias('departure_count'))
    return_count_df = df \
        .groupby('return_name') \
        .count() \
        .select(col('return_name').alias('station_name'),
                col('count').alias('return_count'))
    return departure_count_df \
        .join(return_count_df, on='station_name', how='left') \
        .fillna(0, ['departure_count', 'return_count'])


def save_metrics(metrics_df: DataFrame,
                 path_to_file: str) -> None:
    metrics_df.toPandas().to_csv(path_to_file, header=True, index=False)


path_to_data = os.getenv('PATH_TO_HELSINKI_CITY_BIKES_FILE')
path_to_metrics_file = os.getenv('PATH_TO_METRICS_FILE')

spark_session = SparkSession.builder \
    .getOrCreate()

metrics = compute_metrics(path_to_data, spark_session)
save_metrics(metrics, path_to_metrics_file)
