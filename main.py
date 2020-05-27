import json
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required
from flask import Flask, request, render_template, redirect, flash, url_for
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 

from models import db, User, Post, UserReact

''' Begin boilerplate code '''

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

''' End Flask Login Functions '''

def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  #app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) # uncomment if using flsk jwt
  CORS(app)
  login_manager.init_app(app) # uncomment if using flask login
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()
db.create_all(app=app)

''' End Boilerplate Code '''

''' Set up JWT here (if using flask JWT)'''
'''
#found in lab 5
def authenticate(uname, password): #search for the specified user
  user = User.query.filter_by(username=uname).first() #if user is found and password matches
  if user and user.check_password(password):
    return user 

#Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
  return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)
'''
''' End JWT Setup '''

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/app')
def client_app():
  return app.send_static_file('app.html')


@app.route("/login", methods=(['GET', 'POST']))
def login():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        userData = request.form.to_dict()
        print(userData)
        username = userData['username']
        password = userData['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash('Logged in successfully')
            login_user(user)
            return redirect(url_for ('client_app'))
        if user is None:
            flash('You haven\'t registered yet')
        flash('Invalid login')
        return redirect(url_for('login'))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
