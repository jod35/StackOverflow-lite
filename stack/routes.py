from . import app,db,bcrypt
from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,current_user
from .models import User,Question



@app.route('/')
def index():
    questions=Question.query.filter_by(author=current_user).limit(10).all()
    return render_template('index.html',questions=questions)

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_user=User(
            full_name=request.form.get('full_name'),
            username=request.form.get('username'),
            email=request.form.get('email'),
            password=bcrypt.generate_password_hash(request.form.get('password')))

        db.session.add(new_user)
        db.session.commit()
        flash('Account Has Been Created Successfully')
        return redirect('signup')

    return render_template('sign.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    username=request.form.get('username')
    password=request.form.get('password')

    user=User.query.filter_by(username=username).first()


    if user and bcrypt.check_password_hash(user.password,password):
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



#ask questions
@app.route('/ask',methods=['POST'])
def ask():
    title=request.form.get('title')
    description=request.form.get('description')
    new_question=Question(title=title,content=description,author=current_user)
    db.session.add(new_question)
    db.session.commit()
    flash("Question Asked! Wait for the replies.")
    return redirect(url_for('ask'))

@app.route('/ask_questions')
def ask_page():
    return render_template('ask.html')