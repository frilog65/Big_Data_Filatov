FROM apache/airflow:2.5.3
USER root
RUN apt-get update && apt-get install gcc g++ libsasl2-dev -y
RUN python3 -m pip install --upgrade pip
USER airflow
COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt
