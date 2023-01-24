# Localstack

## How to run it

First you need to download the [dataset](https://www.kaggle.com/datasets/geometrein/helsinki-city-bikes). After that put
database.csv in project root folder

Run

```shell
source .env
python scripts/split_csv.py
```

Next

```shell
make build
```

and after all services are started, you can go
to [airflow-webserver](http://10.5.2.1:8080), [spark-master-web-ui](http://10.5.1.1:8080) and
check [helsinki-city-bikes](http://10.5.0.2:4566/helsinki-city-bikes) bucket

To stop all services enter

```shell
make down
```

## Results

### After all services have started

Data directory:

![data](images/data.png)

Docker services:

![docker-services](images/docker-sevices.png)

Airflow webserver:

![airflow](images/airflow.png)

Spark master web ui:

![spark-master](images/spark-master.png)

### After airflow dag has completed

Aiflow dag:

![dag](images/dag.png)

S3 bucket:

![s3-bucket](images/s3-bucket.png)

Running lambdas:

![running-lambda-1](images/running-lambda-1.png)

![running-lambda-2](images/running-lambda-2.png)

Writing to dynamodb:

![dynamodb-write](images/dynamodb-write.png)

Scan of helsinki_city_bikes_monthly_metrics table:

![monthly-metrics](images/monthly-metrics.png)

Completed spark application:

![spark-applications](images/spark-applications.png)

Tableau visualisation:

![tableau](images/tableau.png)
