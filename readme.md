# Flask Task

## _A Task from, BilliMD_

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

## Pre Requisites

- MongoDB
- Python3

## Instalation

Before instalation please install Pipenv for dependency resolution.

```sh
pip install --user pipenv
```

Clone this repo and go into the folder

```zsh
git clone https://github.com/rayfranc/flask-task.git
cd flask-task
```

Create an ".env" file and add the following required variables and their respectives values

```txt
SECRET_KEY =
JWT_SECRET_KEY =
JWT_TOKEN_LOCATION =
MONGO_DB_URL=
MONGO_DB_PORT=
```

Now install the dependencies and activate vitual env

```sh
pipenv install
pipenv shell
```

For running the code you only need to do.

```sh
flask run
```

## Features

- CRUD Method over user documents
- JWT Authentication

## [Documentation](https://documenter.getpostman.com/view/23290368/2sAXqtaLhc)
