# docker-flask-postgres

This is a simple demo for how to connect to a Postgres database from a python flask application. To run this on your computer you must first install [docker](https://docs.docker.com/engine/installation/).

## Running

You should also have [docker](https://docs.docker.com/install/). If you're on linux, you probably also want docker-compose. Last I checked (over a year ago) it did not come with docker by default. For Mac and Windows you get it with the default installation.

Once you have all of that, you should be good. No need to install [Postgres](https://www.postgresql.org/) or even Python.

```
sudo docker-compose build --no-cache   # Run the container.

sudo docker-compose up

docker-compose down   # Stop and remove everything.


sudo docker-compose run web db init

sudo docker-compose run web db migrate -m "initial migration"


...


## How it works

There are two Dockerfiles. One is the base Dockerfile that has Python and Flask. I've separated that one out so you don't have to keep downloading Python and Flask over and over again. The second one is the application Dockerfile. This is the one that will get updated frequently as you make changes to your Flask app. I found this to be a faster, more convenient iteration cycle for when I was building it.

The `docker-compose.yml` file tells Docker that you need your Flask container and a Postgres container.


<dl>
	<dt><H2>List install</H2></dt>
</dl>


```sudo docker-compose up -d```


```sudo docker-compose up```

sudo docker exec -i -t CONTAINER_ID /bin/bash


su - postgres



psql -h localhost -p 5432 postgres


sudo docker rm -v flaskblog_db_1

sudo docker-compose up -d --force-recreate

