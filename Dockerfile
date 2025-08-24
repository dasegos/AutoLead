FROM python:3.12.8

COPY . .
WORKDIR .

RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

EXPOSE 8000