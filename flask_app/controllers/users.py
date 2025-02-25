from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/registerpage', methods=['GET', 'POST'])
def registerPage():
    if 'user_id' in session:
        return redirect('/')
    if request.method == 'POST':
        # Handle registration logic here
        if 'user_id' in session:
            return redirect('/')

        # Check if the email already exists
        if User.get_user_by_email(request.form['email']):
            flash('This email already exists. Try another one.', 'register_error')
            return redirect('/registerpage')

        # Validate registration input
        if not User.validate_registration(request.form):
            return redirect('/registerpage')

        # Hash the password using bcrypt
        hashed_pw = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')  # Ensure it's decoded as a string

        # Create the user data
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": hashed_pw,
        }

        # Save the user to the database
        user_id = User.create_user(data)

        # Flash success message and redirect
        flash("Account created successfully!", "register_success")
        return redirect('/loginpage')

    # If GET request, simply render the registration form
    return render_template('register.html')

# Route to handle the login page and login process
@app.route('/loginpage')
def LoginPage():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def Login():
    if 'user_id' in session:
        return redirect('/dashboard')

    user = User.get_user_by_email(request.form['email'])
    if not user:
        flash("Invalid email or password.", "login_error")
        return redirect('/loginpage')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid email or password.", "login_error")
        return redirect('/loginpage')

    session['user_id'] = user.id
    print("Logged in User ID:", session['user_id'])
    return redirect('/dashboard')
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')


@app.context_processor
def inject_user():
    if 'user_id' in session:
        user = User.get_user_by_id(session['user_id'])
        if user:
            return {'current_user': user}
    return {}
