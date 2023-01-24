import json
import os

import boto3
import pandas as pd


def lambda_handler(event, context):
    aws_endpoint_url = os.getenv('AWS_ENDPOINT_URL')
    aws_access_key = os.getenv('AWS_ACCESS_KEY')
    aws_secret_key = os.getenv('AWS_SECRET_KEY')
    aws_region_name = os.getenv('AWS_REGION_NAME')
    s3_resource = boto3.resource('s3',
                                 endpoint_url=aws_endpoint_url,
                                 aws_access_key_id=aws_access_key,
                                 aws_secret_access_key=aws_secret_key,
                                 region_name=aws_region_name)
    dynamodb_resource = boto3.resource('dynamodb',
                                       endpoint_url=aws_endpoint_url,
                                       aws_access_key_id=aws_access_key,
                                       aws_secret_access_key=aws_secret_key,
                                       region_name=aws_region_name)
    helsinki_city_bikes_station_metrics_table = dynamodb_resource.Table('helsinki_city_bikes_station_metrics')
    event_body = event['Records'][0]['body']
    helsinki_city_bikes_metrics_key = json.loads(event_body)['Records'][0]['s3']['object']['key']
    helsinki_city_bikes_metrics_df = pd.read_csv(s3_resource.Object(bucket_name='helsinki-city-bikes',
                                                                    key=helsinki_city_bikes_metrics_key)
                                                 .get()['Body']) \
        .fillna(0)
    with helsinki_city_bikes_station_metrics_table.batch_writer(overwrite_by_pkeys=['station_name']) as batch_writer:
        for _, row in helsinki_city_bikes_metrics_df.iterrows():
            batch_writer.put_item(Item={'station_name': row['station_name'],
                                        'departure_count': int(row['departure_count']),
                                        'return_count': int(row['return_count'])})
