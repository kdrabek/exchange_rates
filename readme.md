## Exchange Rates

The application periodically fetches exchange rates from Polish National Bank's open REST API (http://api.nbp.pl/en.html) and persists them in PostgresDB. It then exposes its REST API that facilitates various getting information as well as creating automatic email notifications when certain criteria are met. 

It was written for _educational_ puroposes only.

### Running the application

```
cd docker
docker$ docker-compose build
docker$ docker-compose up -d
```

### Running tests
Provided the images are build, tests for the entire project can be run like below:
```
cd docker
docker$ docker-compose up -d shell
docker$ ./exec_tests.sh
```

Running tests for single application:
```
cd docker
docker$ docker-compose up -d
docker$ ./exec_tests.sh notifications/
```

### Running the dev enviroment

There's a dedicated docker-compose service for development work, which has access to the DB and RabbitMQ only:
```
cd docker
docker$ docker-compose up -d shell
```

### Running the web app
The web docker-compose service has access to the nginx and Django

```
cd docker
docker$ docker-compose up -d web
```
