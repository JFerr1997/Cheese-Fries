from flask import Flask,flash
import re
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX=re.compile(r'^[a-zA-Z]+$')


class User:
    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']


    @staticmethod
    def validate_user(user):
        is_valid= True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipes').query_db(query,user)
        if len(user['first_name']) < 3:
            flash("First name must be 3 or more characters")
            is_valid=False
        if not NAME_REGEX.match(user['first_name']):
            flash('Invalid name')
            is_valid=False
        if len(user['last_name']) < 3:
            flash("Last name must be 3 or more characters")
            is_valid=False
        if not NAME_REGEX.match(user['last_name']):
            flash('Invalid name')
            is_valid=False
        if len(user['email']) < 3:
            flash("Must be a valid email format")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address")
            is_valid=False
        if len(results) >= 1:
            flash("Email already in use.")
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters long')
            is_valid=False
        if user['confirm_password'] != user['password']:
            is_valid=False
        return is_valid

    @classmethod
    def save(cls,data):
        query="INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        return connectToMySQL('recipes').query_db( query, data )

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL('recipes').query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query,data)
        return cls(results[0])


