from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made_on = data['date_made_on']
        self.under_thirty_minutes = data['under_thirty_minutes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    @staticmethod
    def validate_recipe(name, description, instructions, date_made_on):
        is_valid = True
        if name == '':
            flash("Must enter a name.", "add_recipe")
            is_valid = False
        if not name == '':
            if len(name) < 3:
                flash("Name must be at least 3 characters.", "add_recipe")
                is_valid = False
        if description == '':
            flash("Must enter a description.", "add_recipe")
            is_valid = False
        if not description == '':
            if len(name) < 3:
                flash("Description must be at least 3 characters.", "add_recipe")
                is_valid = False
        if instructions == '':
            flash("Must enter instructions.", "add_recipe")
            is_valid = False
        if not instructions == '':
            if len(name) < 3:
                flash("Instructions must be at least 3 characters.", "add_recipe")
                is_valid = False
        if date_made_on == '':
            flash("Must enter a date.", "add_recipe")
            is_valid = False
        return is_valid
    @classmethod
    def add_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made_on, under_thirty_minutes, created_at, updated_at, user_id) VALUE (%(name)s, %(description)s, %(instructions)s, %(date_made_on)s, %(under_thirty_minutes)s, NOW(), NOW(), %(user_id)s)"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return results
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM RECIPES"
        results = connectToMySQL('recipes_schema').query_db(query)
        all_recipes = []
        for recipe in results:
            all_recipes.append(recipe)
        return all_recipes
    @classmethod
    def get_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return cls(results[0])
    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made_on = %(date_made_on)s, under_thirty_minutes = %(under_thirty_minutes)s, updated_at = NOW() WHERE id = %(id)s"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return results
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        results = connectToMySQL('recipes_schema').query_db(query, data)
        return results