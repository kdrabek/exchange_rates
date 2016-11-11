FROM python:3.5
ADD requirements.txt /app/requirements.txt
ADD requirements_dev.txt /app/requirements_dev.txt

WORKDIR /app/

RUN pip install -r requirements.txt
RUN pip install -r requirements_dev.txt
RUN adduser --disabled-password --gecos "" exchange
