from . import app,db,bcrypt
from flask_login import login_user,logout_user,current_user
from flask import render_template,redirect,url_for,request,flash
from .models import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        confirm=request.form['confirm']

        new_user=User(
            username=username,
            email=email,
            password=bcrypt.generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account Created Successfully!!")
        return redirect('signup')
    return render_template('sign.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    email=request.form.get('prompt')
    user=User.query.filter_by(email=email).first()
    password=request.form.get('password')
    if user and bcrypt.check_password_hash(password,user.password):
        login_user(user)
        return "Logged In"
    return render_template('login.html')
