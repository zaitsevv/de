FROM apache/spark-py:3.3.1

USER root

RUN pip install pandas==1.5.2

USER 185
