from . import app,db
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

        user=User.query.filter_by(username=username).first()

        if user:
            flash("Account with email {} exists".format(user.email))
            return redirect(url_for('signup'))
        
        else:
            new_user=User(
                username=username,
                email=email,
                password=password,
            )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Account Created Successfully, You can Login")

        



    

    
    return render_template('sign.html')

@app.route('/login')
def login():
    return render_template('login.html')
