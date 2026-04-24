from functools import wraps
from flask import render_template, redirect, request, session, flash
from flask_app import app, bcrypt
from flask_app.models.user import User

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/loginpage')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect('/dashboard')

@app.route('/loginpage')
def login_page():
    return render_template('login.html')

@app.route('/registerpage')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/registerpage')

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email({"email": request.form['email']})

    if not user or not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/loginpage')

    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/loginpage')

@app.context_processor
def inject_user():
    if 'user_id' in session:
        user = User.get_by_id({'id': session['user_id']})
        return {'current_user': user}
    return {'current_user': None}
