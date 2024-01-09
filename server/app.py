#!/usr/bin/env python3

from flask import Flask, jsonify, request, session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from models import db, User, Chat, HealthConditions, Treatment

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

db.init_app(app)

URL_PREFIX = '/api'

# HELPER METHOD #

def current_user():
    if session["user_id"]:
        return User.query.filter(User.id == session["user_id"]).first()


# USER SIGNUP #

@app.post(URL_PREFIX + '/users')
def create_user():
    try:
        data = request.json
        password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(email=data['email'], password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
        return new_user.to_dict(), 201
    except Exception as e:
        return { 'error': str(e) }, 406


# SESSION LOGIN/LOGOUT#

@app.post(URL_PREFIX + '/login')
def login():
    data = request.json
    user = User.query.filter(User.email == data["email"]).first()
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        session["user_id"] = user.id
        return user.to_dict(), 201
    else:
        return { "message": "Invalid username or password" }, 401
    

@app.get(URL_PREFIX + '/check_session')
def check_session():
    user_id = session.get("user_id")
    user = User.query.filter(User.id == user_id).first()
    if user:
        return user.to_dict(), 200
    else:
        return { "message": "No logged in user" }, 401
    

@app.delete(URL_PREFIX + '/logout')
def logout():
    session.pop('user_id')
    return {}, 204


# EXAMPLE OTHER RESOURCES #

@app.get(URL_PREFIX + '/chats')
def get_chats():
    return jsonify( [chat.to_dict() for chat in current_user().chats] ), 200

@app.post(URL_PREFIX + '/chats')
def create_chat():
    try:
        data = request.json
        new_chat = Chat(**data)
        new_chat.user = current_user()
        db.session.add(new_chat)
        db.session.commit()
        return jsonify( new_chat.to_dict() ), 201
    except Exception as e:
        return jsonify( {'error': str(e)} ), 406


#----- Health Conditions Routes ------#
    
@app.route('/healthconditions', methods=['GET'])
def get_health_conditions():
    health_conditions = HealthConditions.query.all()
    return jsonify([health_condition.to_dict() for health_condition in health_conditions]), 200

@app.route('/healthconditions/<int:healthcondition_id>', methods=['GET'])
def get_health_condition(healthcondition_id):
    health_condition = HealthConditions.query.get(healthcondition_id)
    if health_condition:
        return jsonify(health_condition.to_dict()), 200
    else:
        return {'error': 'Health condition not found'}, 404

@app.route('/healthconditions', methods=['POST'])
def create_health_condition():
    try:
        data = request.json
        new_health_condition = HealthConditions(**data)
        db.session.add(new_health_condition)
        db.session.commit()
        return jsonify(new_health_condition.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 406
    

# --- Treatment Routes --- #

@app.route('/treatments', methods=['GET'])
def get_treatments():
    treatments = Treatment.query.all()
    return jsonify([treatment.to_dict() for treatment in treatments]), 200

@app.route('/treatments/<int:treatment_id>', methods=['GET'])
def get_treatment(treatment_id):
    treatment = Treatment.query.get(treatment_id)
    if treatment:
        return jsonify(treatment.to_dict()), 200
    else:
        return {'error': 'Treatment not found'}, 404

@app.route('/treatments', methods=['POST'])
def create_treatment():
    try:
        data = request.json
        new_treatment = Treatment(**data)
        db.session.add(new_treatment)
        db.session.commit()
        return jsonify(new_treatment.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 406
# APP RUN #

if __name__ == '__main__':
    app.run(port=5555, debug=True)