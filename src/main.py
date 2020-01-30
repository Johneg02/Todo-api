"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/todos/user/<username>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def handle_todos(username):

    headers = {
        Content-Type: "application/json"
    }

    requesting_user = User.query.filter_by(username=username).all()
    if request.method=='GET': 
        if len(requesting_user) <1:
            print("Usuario no existe")
            response_body= {
                "status":"HHTP_404_NOT_FOUND. Usuario no existe"

            }
            status_code = 404
        else:
            print("Usuario Existe")
            user_tasks_list = Task.query.filter_by(user_username=username).all()
            response_body = []
            for task in user_tasks_list:
                response_body.append(task.serialize())
            status_code = 200

    elif request.method=='POST': 
        if len(requesting_user) >0:      
            response_body = {
                "status": "HTTP_400_BAD_REQUEST. Usuario ya existe"
            }
            status_code = 400

        elif request.json != []:

            response_body = {
                "status": "HTTP_400_BAD_REQUEST. Datos inesperados para crear usuario"
            }    
            status_code = 400
        
        else:

            print("Creando usuario con una tarea")
            new_user = User(username)
            new_user.username = username
            db.session.add(new_user)
            sample_task = Task("sample task", new_user.username)
            db.session.add(sample_task)
            db.session.commit()
            response_body = {
                "status": "ok"
            }
            status_code = 200
                   

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
