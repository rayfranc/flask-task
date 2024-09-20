from os import environ

SECRET_KEY = environ.get('SECRET_KEY')
JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
JWT_TOKEN_LOCATION = environ.get('JWT_TOKEN_LOCATION')
MONGO_DB_URL=environ.get('MONGO_DB_URL')
MONGO_DB_PORT=environ.get("MONGO_DB_PORT")
