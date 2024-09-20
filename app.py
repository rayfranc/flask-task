import json
from marshmallow import ValidationError
from pymongo.errors import ServerSelectionTimeoutError
import uuid
from models import UserSchema
from flask import Flask, request, jsonify, Response, session
from pymongo import MongoClient
from datetime import datetime
from settings import MONGO_DB_URL, MONGO_DB_PORT
from bson import json_util, ObjectId
from crypt import Crypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.exceptions import HTTPException, NotFound, BadRequest

app = Flask(__name__)

app.config.from_pyfile('settings.py')
print(MONGO_DB_URL)

client = MongoClient(MONGO_DB_URL, int(MONGO_DB_PORT))

jwt = JWTManager(app)


db = client.flask_db

users_db = db.users

Crypt().setup(app)


@app.errorhandler(HTTPException)
def handle_exception(e):

    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.errorhandler(ServerSelectionTimeoutError)
def handle_db_error(e):
    return Response(json.dumps({
        "code": 500,
        "name": "Database not Found",
        "description": "Server have no access to database please review your network configuration ",
    }), status=500, mimetype="application/json")


# Authentication Routes
@app.post('/login')
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    print('Received data:', username, password)
    if not (username == 'admin' and password == "password"):
        user = users_db.find_one({"first_name": username})

        if user and Crypt().check_hash(user['password'], password):
            session['session_id'] = str(uuid.uuid4())
            session['user_id'] = json.loads(json_util.dumps(user['_id']))
            session['logged_in'] = True
            access_token = create_access_token(identity=session['session_id'])
            return jsonify({'message': 'Login Success', 'access_token': access_token, 'session_id': session['session_id']})
        else:
            return jsonify({'message': 'Login Failed'}), 401
    else:
        if session.get('logged_in'):
            raise BadRequest('User already authenticated')
        session['session_id'] = str(uuid.uuid4())
        session['logged_in'] = True
        access_token = create_access_token(identity=session['session_id'])
        return jsonify({'message': 'Login Success', 'access_token': access_token, 'session_id': session['session_id']})


@app.post("/logout")
@jwt_required()
def logout():
    session.clear()
    return jsonify({'message': 'Logout Success'})


@app.get("/user")
def get_users():
    users = []
    for user in users_db.find():
        users.append(user)
    return json.loads(json_util.dumps(users))


@app.get("/user/<id>")
def get_one_user(id):
    record = users_db.find_one({"_id": ObjectId(id)})
    if not record:
        raise NotFound("No user Found")
    return json.loads(json_util.dumps(record))


@app.post('/user')
def createUser():
    data = request.json
    schema = UserSchema()
    try:
        result = schema.load(data)
        print(result.to_json())
        id = users_db.insert_one(
            {**result.to_json(), "created_at": datetime.now(), "updated_at": datetime.now()})
        result._id = id.inserted_id
        return Response(json_util.dumps({"id": result._id}), status=201, mimetype='application/json')
    except ValidationError as err:
        # Return a nice message if validation fails
        return jsonify(err.messages), 400


@app.put('/user/<id>')
@jwt_required()
def updateUser(id):
    if not session:
        return jsonify({"message": 'User not authenticated'}), 401
    data = request.json
    schema = UserSchema()
    try:
        user = schema.load(data, partial=True)
        print(user.to_json())
        user_json = user.to_json()
        for key in list(user_json.keys()):
            if user_json[key] is None:
                del user_json[key]
        id = users_db.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
                                          **user_json, "updated_at": datetime.now(), 'session_token': str(session['session_id'])}}, upsert=True)
        if not id:
            raise NotFound('User not found')
        return jsonify({"message": "success"}), 200
    except ValidationError as err:
        return jsonify(err.messages), 400


@app.delete('/user/<id>/')
@jwt_required()
def delete(id):
    record = users_db.find_one_and_delete({"_id": ObjectId(id)})
    if not record:
        raise NotFound("No user Found")
    return jsonify({"message": "success"}), 200
