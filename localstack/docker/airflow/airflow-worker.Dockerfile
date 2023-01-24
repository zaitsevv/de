FROM apache/airflow:2.5.0

USER root

RUN apt update && \
    apt install -y openjdk-11-jdk && \
    apt clean

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

USER airflow

RUN pip install \
    apache-airflow-providers-amazon==7.0.0 \
    apache-airflow-providers-apache-spark==4.0.0
