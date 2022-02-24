from flask import Flask, redirect, render_template, request, session, flash
from flask_app.models import user
from flask_app.models import recipe
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'Invalid URL.'

@app.route('/')
def index():
    if 'logged_in' not in session:
        return redirect('/login_register')
    return redirect('/dashboard')

@app.route('/login_register')
def login_register():
    if 'logged_in' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'logged_in' not in session:
        return redirect('/login_register')
    return render_template('dashboard.html', all_recipes = recipe.Recipe.get_all_recipes())

@app.route('/register_submission', methods=['POST'])
def register_submission():
    if request.form['email'] in user.User.get_all_emails():
        flash("That email is already registered.", "register")
        return redirect('/')
    if not user.User.validate_user(request.form['fname'], request.form['lname'], request.form['email'], request.form['password'], request.form['pass_confirm']):
        return redirect('/login_register')
    password_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'fname' : request.form['fname'],
        'lname' : request.form['lname'],
        'email' : request.form['email'],
        'password' : password_hash
    }
    user_id = user.User.register_user(data)
    session['user_id'] = user_id
    session['name'] = f"{request.form['fname']} {request.form['lname']}"
    session['logged_in'] = True
    return redirect('/')

@app.route('/login_submission', methods=['POST'])
def login_submission():
    if request.form['login_email'] == '':
        flash("Must enter an email address.", "login")
        return redirect('/')
    if request.form['login_password'] == '':
        flash("Must enter a password.", "login")
        return redirect('/')
    data = {
        'email' : request.form['login_email']
    }
    user_in_db = user.User.get_user(data)
    if not user_in_db:
        flash("Invalid email/password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(str(user_in_db.password), request.form['login_password']):
        flash("Invalid email/password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['name'] = f"{user_in_db.first_name} {user_in_db.last_name}"
    session['logged_in'] = True
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')