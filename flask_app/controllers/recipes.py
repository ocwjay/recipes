from flask import Flask, redirect, render_template, request, session, flash
from flask_app.models import recipe
from flask_app import app

@app.route('/create_recipe')
def create_recipe():
    if 'logged_in' not in session:
        return redirect('/login_register')
    return render_template("add_recipe.html")

@app.route('/recipe/<int:id>')
def view_recipe(id):
    if 'logged_in' not in session:
        return redirect('/login_register')
    data = {
        'id' : id
    }
    return render_template("recipe.html", recipe = recipe.Recipe.get_recipe(data))

@app.route('/edit_recipe/<int:id>')
def edit_recipe(id):
    if 'logged_in' not in session:
        return redirect('/login_register')
    data = {
        'id' : id
    }
    return render_template("edit_recipe.html", recipe = recipe.Recipe.get_recipe(data))

@app.route('/create_recipe_submit', methods=['POST'])
def create_recipe_submit():
    if not recipe.Recipe.validate_recipe(request.form['recipe_name'], request.form['recipe_description'], request.form['recipe_instructions'], request.form['recipe_date_made']):
        return redirect('/create_recipe')
    data = {
        'name' : request.form['recipe_name'],
        'description' : request.form['recipe_description'],
        'instructions' : request.form['recipe_instructions'],
        'date_made_on' : request.form['recipe_date_made'],
        'under_thirty_minutes' : request.form['radio'],
        'user_id' : request.form['user_id']
    }
    recipe.Recipe.add_recipe(data)
    return redirect('/dashboard')

@app.route('/edit_recipe_submission/<int:id>', methods=['POST'])
def edit_recipe_submission(id):
    data = {
        'id' : id,
        'name' : request.form['recipe_name'],
        'description' : request.form['recipe_description'],
        'instructions' : request.form['recipe_instructions'],
        'date_made_on' : request.form['recipe_date_made'],
        'under_thirty_minutes' : request.form['radio']
    }
    if not recipe.Recipe.validate_recipe(request.form['recipe_name'], request.form['recipe_description'], request.form['recipe_instructions'], request.form['recipe_date_made']):
        return redirect(f"/edit_recipe/{data['id']}")
    recipe.Recipe.edit_recipe(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete(id):
    data = {
        'id' : id
    }
    recipe.Recipe.delete_recipe(data)
    return redirect('/dashboard')