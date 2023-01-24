import json
import os
from decimal import Decimal

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
    helsinki_city_bikes_raw_table = dynamodb_resource.Table('helsinki_city_bikes_raw')
    event_body = event['Records'][0]['Sns']['Message']
    helsinki_city_bikes_key = json.loads(event_body)['Records'][0]['s3']['object']['key']
    helsinki_city_bikes_df = pd.read_csv(s3_resource.Object(bucket_name='helsinki-city-bikes',
                                                            key=helsinki_city_bikes_key)
                                         .get()['Body']) \
        .fillna(0)
    with helsinki_city_bikes_raw_table.batch_writer(overwrite_by_pkeys=['departure_id', 'return_id']) as batch_writer:
        for _, row in helsinki_city_bikes_df.iterrows():
            batch_writer.put_item(Item={'departure': row['departure'],
                                        'return': row['return'],
                                        'departure_id': int(row['departure_id']),
                                        'departure_name': row['departure_name'],
                                        'return_id': int(row['return_id']),
                                        'return_name': row['return_name'],
                                        'distance (m)': int(row['distance (m)']),
                                        'duration (sec.)': int(row['duration (sec.)']),
                                        'avg_speed (km/h)': Decimal(str(row['avg_speed (km/h)'])),
                                        'departure_latitude': Decimal(str(row['departure_latitude'])),
                                        'departure_longitude': Decimal(str(row['departure_longitude'])),
                                        'return_latitude': Decimal(str(row['return_latitude'])),
                                        'return_longitude': Decimal(str(row['return_longitude'])),
                                        'Air temperature (degC)': Decimal(str(row['Air temperature (degC)']))})
