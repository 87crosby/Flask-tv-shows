from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models.users import User


class Show():

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = None

    @classmethod
    def get_all_shows(cls):
        query = "SELECT * FROM shows"

        result = connectToMySQL('exam_schema').query_db(query)

        return result

    @classmethod
    def create_show(cls, data):
        query = "INSERT INTO shows(name, description, network, release_date, users_id) VALUES (%(name)s, %(description)s, %(network)s, %(release_date)s, %(users_id)s);"

        result = connectToMySQL('exam_schema').query_db(query, data)

        return result

    @classmethod
    def get_shows_by_id(cls,data):
        query = "SELECT * FROM users JOIN shows ON shows.users_id = users.id WHERE shows.id = %(id)s"

        result = connectToMySQL('exam_schema').query_db(query, data)
        #print(result[0])

        return result[0]

    @classmethod
    def update_show(cls,data):
        query = 'UPDATE shows SET name = %(name)s, description = %(description)s, network = %(network)s, release_date = %(release_date)s WHERE id = %(id)s;'

        connectToMySQL('exam_schema').query_db(query, data)

    @classmethod
    def delete_show(cls,data):
        query = 'DELETE FROM shows WHERE id = %(id)s;'

        connectToMySQL('exam_schema').query_db(query, data)
    


    @staticmethod
    def validate_show(data):
        is_valid = True

        if len(data['name']) < 3 or len(data['name']) > 100:
            flash("Show name should be 1 to 100 characters.")
            is_valid = False

        if len(data['description']) < 3:
            flash("Show description should be at least 3 characters")
            is_valid = False

        if len(data['network']) < 3:
            flash("Show Network should be at least 3 characters")
            is_valid = False

        if len(data['release_date']) == 0:
            flash("Please provide a date.")
            is_valid = False

        return is_valid