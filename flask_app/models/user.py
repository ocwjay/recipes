from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = ['updated_at']
    @staticmethod
    def validate_user(first_name, last_name, email, password, pass_confirm):
        is_valid = True
        if first_name == '':
            flash("Must enter a first name.", 'register')
            is_valid = False
        if not first_name == '':
            if len(first_name) < 2:
                flash("First name must be at least 2 characters.", 'register')
                is_valid = False
        if last_name == '':
            flash("Must enter a last name.", 'register')
            is_valid = False
        if not last_name == '':
            if len(last_name) < 2:
                flash("Last name must be at least 2 characters.", 'register')
                is_valid = False
        if email == '':
            flash("Must enter an email address.", 'register')
            is_valid = False
        if not email == '':
            if not EMAIL_REGEX.match(email):
                flash("Must enter a valid email address.", 'register')
                is_valid = False
        if password == '':
            flash("Must enter a password.", 'register')
            is_valid = False
        if not password == '':
            if not password == pass_confirm:
                flash("Passwords must match.", 'register')
                is_valid = False
        return is_valid
    @classmethod
    def register_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUE (%(fname)s, %(lname)s, %(email)s, %(password)s, NOW(), NOW())"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        print(results)
        return results
    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return cls(results[0])
    @classmethod
    def get_all_emails(cls):
        query = "SELECT email FROM users"
        results = connectToMySQL('recipes_schema').query_db(query)
        all_emails = []
        for email in results:
            all_emails.append(email['email'])
        return all_emails