# Bell Project App

This demo application is created using [vuejs](https://vuejs.org/) v2.x,
[flask](https://flask.palletsprojects.com/), and [redis](https://redis.com/).
[nginx](https://www.nginx.com/) is the proxy server for hosting both the
frontend and the backend.

## Prerequisite

The following pre-requisites are required to build and run this application.

- [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/linux/)
- [nodejs](https://nodejs.org/en/download/) with npm

## Structure of the this repo

- The directory `myapp` contains all python modules for running the backend.
- The directory `src` contains all source code for building the UI artifacts.
- The file `Dockerfile` builds the docker image for hosting the backend through [uwsgi](https://uwsgi-docs.readthedocs.io/).
- The file `nginx-conf/default.conf` shows how nginx is configured in its container.
- The file `docker-compose.yaml` is the docker-compose file for running the whole application. See the next section.

## Setup the production environment

### Build the docker image and the UI assets

Run the following command to build the doker image.
```
docker-compose build
```

Run the following command to build the UI assets.
```
npm install
npm run build
```

### Run the app

Run the following command to start the application.
```
docker-compose up
```

## Setup the development environment

[Python](https://www.python.org/downloads/) v3.10 is required for the backend development.

Run the following command to bring up the development server for the backend.

```
pip install -r myapp/requirements.txt
cd myapp && python app.py
```
Run the following commands to bring up the development server for the frontend.

```
npm install
npm run serve
```
