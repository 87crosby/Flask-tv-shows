import re

from flask.helpers import flash
from flask_app import app
from flask import render_template, redirect, session, request
from flask_bcrypt import Bcrypt
from flask_app.models.users import User

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/register', methods = ['POST'])
def register_user():
    
    if User.validate_registration(request.form):
        #hash password
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        
        User.create_user(data)
    return redirect('/')

@app.route('/users/login', methods = ['POST'])
def login_user():

    users = User.get_users_with_email(request.form)

    if len(users) != 1:
        flash("User doesn't exist")
        return redirect('/')
    
    user = users[0]

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Password")
        return redirect('/')

    session['user_id'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session['email'] = user.email

    return redirect('/dashboard')
    


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')