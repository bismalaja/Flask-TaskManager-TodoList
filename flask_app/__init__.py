from flask import Flask, render_template, redirect, request, session, flash
import os
from flask_app.config.sqliteconnection import init_db
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'super_secret_key')
bcrypt = Bcrypt(app)

init_db()
