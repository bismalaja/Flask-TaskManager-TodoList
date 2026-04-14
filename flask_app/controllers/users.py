from flask import redirect, session
from flask_app import app

LOCAL_USER = {
    "id": 1,
    "first_name": "Local",
    "last_name": "User",
}


@app.before_request
def ensure_local_user():
    session.setdefault("user_id", LOCAL_USER["id"])

@app.route('/')
def index():
    return redirect('/dashboard')

@app.route('/registerpage', methods=['GET', 'POST'])
def registerPage():
    return redirect('/dashboard')

@app.route('/loginpage')
def LoginPage():
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def Login():
    session['user_id'] = LOCAL_USER['id']
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session['user_id'] = LOCAL_USER['id']
    return redirect('/dashboard')


@app.context_processor
def inject_user():
    return {'current_user': LOCAL_USER}
