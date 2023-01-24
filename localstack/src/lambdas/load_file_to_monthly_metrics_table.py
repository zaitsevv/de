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
    helsinki_city_bikes_monthly_metrics_table = dynamodb_resource.Table('helsinki_city_bikes_monthly_metrics')
    event_body = event['Records'][0]['Sns']['Message']
    helsinki_city_bikes_key = json.loads(event_body)['Records'][0]['s3']['object']['key']
    helsinki_city_bikes_df = pd.read_csv(s3_resource.Object(bucket_name='helsinki-city-bikes',
                                                            key=helsinki_city_bikes_key)
                                         .get()['Body'],
                                         parse_dates=['departure']) \
        .fillna(0)
    helsinki_city_bikes_date = f"{helsinki_city_bikes_df['departure'][0]:%Y-%m}-01"
    helsinki_city_bikes_monthly_metrics_table.put_item(
        Item={'date': helsinki_city_bikes_date,
              'avg_distance_m': Decimal(str(helsinki_city_bikes_df['distance (m)'].mean())),
              'avg_duration_sec': Decimal(str(helsinki_city_bikes_df['duration (sec.)'].mean())),
              'avg_speed_km_h': Decimal(str(helsinki_city_bikes_df['avg_speed (km/h)'].mean())),
              'avg_air_temperature_c': Decimal(str(helsinki_city_bikes_df['Air temperature (degC)'].mean()))})
