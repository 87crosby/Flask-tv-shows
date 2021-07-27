from flask import flash
from flask.scaffold import F
from flask_app import app
import re
from flask_app.config.mysqlconnection import connectToMySQL

class User():

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    

    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        
        result = connectToMySQL('exam_schema').query_db(query, data)

        return result
    
    @classmethod
    def get_users_with_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"

        results = connectToMySQL('exam_schema').query_db(query, data)

        users = []
        
        for item in results:
            users.append(User(item))
        
        return users

    @classmethod
    def get_users_with_first_name(cls, data):
        query = "SELECT * FROM users WHERE first_name = %(first_name)s"

        results = connectToMySQL('exam_schema').query_db(query, data)

        users = []
        
        for item in results:
            users.append(User(item))
        
        return users
    
    @staticmethod
    def validate_registration(data):
        '''
        Function that ensures user data is valid
        data = a dictionary
        returns: Boolean
        '''
        is_valid = True
        #fisrt_name longer than 2 chars
        if (len(data['first_name']) < 2):
            flash("First name should be atleast 2 characters")
            is_valid = False

        #last name longer than 2 chars
        if (len(data['last_name']) < 2):
            flash("Last name should be atleast 2 characters")
            is_valid = False
        
        #email should be valid
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not email_regex.match(data['email']):
            flash("Email not valid")
            is_valid = False

        #password minimum length 8 characters
        if len(data['password']) < 8:
            flash("Password should be at least 8 characters")
            is_valid = False

        #confirm password match
        if data['password'] != data['confirm_password']:
            flash("Passwords should match")
            is_valid = False

        #ensure email isn't in use
        if len(User.get_users_with_email({'email': data['email']})) != 0:
            flash("Email already in use")
            is_valid = False


        return is_valid