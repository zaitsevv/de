"""
Script for splitting csv file by months. DATABASE_CSV and HOST_DATA_DIRECTORY variables are contained in the .env file
"""
import os

import pandas as pd

input_path = os.getenv('DATABASE_CSV')
output_path = os.getenv('HOST_DATA_DIRECTORY')

dataframe = pd.read_csv(input_path, parse_dates=['departure'])

for group_name, group in dataframe.groupby(pd.Grouper(key='departure', freq='M')):
    group.to_csv(f'{output_path}/{group_name:%Y-%m}.csv', index=False)
