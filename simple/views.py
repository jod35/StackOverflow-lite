from . import app
from flask import render_template,redirect,url_for,request

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('sign.html')

@app.route('/login')
def login():
    return render_template('login.html')
