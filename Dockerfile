FROM python:3.12.8

WORKDIR /app
COPY requirements.txt .
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
COPY . /app