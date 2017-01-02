FROM python:3.5
ADD requirements.txt /app/requirements.txt
ADD requirements_dev.txt /app/requirements_dev.txt

WORKDIR /app/

ENV NOTIFICATIONS_EMAIL_PASSWORD=$NOTIFICATIONS_EMAIL_PASSWORD
ENV NOTIFICATIONS_EMAIL_USER=$NOTIFICATIONS_EMAIL_PASSWORD

RUN pip install -r requirements.txt
RUN pip install -r requirements_dev.txt
RUN adduser --disabled-password --gecos "" exchange
RUN touch exchange_rates.log
RUN chown exchange:exchange exchange_rates.log
