FROM spark-py:v3.3.0

USER root

ENV PYSPARK_MAJOR_PYTHON_VERSION=3

WORKDIR /opt/application

COPY requirements.txt .
RUN pip install -r requirements.txt --user

COPY src/main.py main.py


