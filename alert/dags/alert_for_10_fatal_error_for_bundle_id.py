from datetime import datetime
from datetime import timedelta

import pandas as pd
from airflow.decorators import dag, task
from airflow.models import Variable


@dag(schedule='0 * * * *',
     start_date=datetime.utcnow(),
     catchup=False)
def alert_for_10_fatal_error_for_bundle_id():
    @task
    def read_csv(path: str) -> pd.DataFrame:
        dataframe = pd.read_csv(path)
        dataframe['23'] = pd.to_datetime(dataframe['23'])
        return dataframe

    @task
    def rename_columns(dataframe: pd.DataFrame, names: dict) -> pd.DataFrame:
        return dataframe.rename(columns=names)

    @task
    def get_data_for_last_hour(dataframe: pd.DataFrame) -> pd.DataFrame:
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        mask = (dataframe['date'] > hour_ago) & \
               (dataframe['date'] <= now)
        return dataframe.loc[mask]

    @task
    def check_for_10_fatal_error_for_bundle_id(dataframe: pd.DataFrame) -> bool:
        return max(dataframe.loc[dataframe['severity'] == 'Error'].groupby(['bundle_id'])['bundle_id'].count(),
                   default=0) < 10

    @task
    def alert() -> None:
        raise Exception('There are more than 10 fatal error in an hour for bundle id')

    path_to_data = Variable.get('PATH_TO_DATA')
    column_names = Variable.get('COLUMN_NAMES', deserialize_json=True)

    dataframe = read_csv(path_to_data)
    renamed_dataframe = rename_columns(dataframe, column_names)
    dataframe_for_last_10_minutes = get_data_for_last_hour(renamed_dataframe)
    check_result = check_for_10_fatal_error_for_bundle_id(dataframe_for_last_10_minutes)
    if not check_result:
        alert()


alert_for_10_fatal_error_for_bundle_id()
