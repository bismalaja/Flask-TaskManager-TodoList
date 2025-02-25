from flask import Flask, render_template, redirect, request, session, flash
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'super_secret_key')
