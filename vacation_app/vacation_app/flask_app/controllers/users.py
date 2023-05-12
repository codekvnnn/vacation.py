from flask_app import app
from flask import render_template,redirect,request,session, flash
from flask_app.models import user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



def name():
    return "name here"

@app.route('/')
def index():
    return redirect('/users/new')

@app.route('/users/dashboard')
def user_dashboard():
    if 'logged_in_id' not in session:
        return redirect('/')
    users = user.User.get_all_users()
    print(users)
    return render_template('user_dashboard.html', all_users = users)

@app.route('/users/show/<int:id>')
def show_user(id):
    if 'logged_in_id' not in session:
        return redirect('/')
    data={
        'id':id
    }
    return render_template('show_user.html', one_user=user.User.get_user_with_trips(data))


@app.route('/users/new')
def new_user():
    return render_template('new_user.html')

@app.route('/users/create', methods=['POST'])
def create_user():
    if not user.User.validate_user(request.form):
        return redirect('/users/new')
    hashed_pw= bcrypt.generate_password_hash(request.form['password'])
    data={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'age':request.form['age'],
        'email':request.form['email'],
        'password':hashed_pw,
    }
    user_id = user.User.create_user(data)
    session['logged_in_id']= user_id
    return redirect('/users/dashboard')


@app.route('/users/login', methods=['POST'])
def user_login():
    one_user=user.User.get_user_by_email(request.form)
    if not one_user:
        flash('Invalid credentials','login')
        return redirect('/users/new')
    if not bcrypt.check_password_hash(one_user.password, request.form['password']):
        flash('Invalid credentials', 'login')
        return redirect('/users/new')
    session['logged_in_id'] = one_user.id
    return redirect(f"/users/show/{one_user.id}")

@app.route('/users/sign_out')
def sign_out():
    session.clear()
    return redirect('/')