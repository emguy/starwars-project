# Bell Project App

## Prerequisite

The following prerequisites are required to build and run this application.

- [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/linux/)
- [nodejs](https://nodejs.org/en/download/) with npm

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
