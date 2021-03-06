from . import app,db
from flask import render_template,redirect,request,url_for,flash
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,current_user
from .models import User,Question,Answer

#home page
@app.route('/')
def index():
    questions=Question.query.order_by(Question.id.desc()).all()
    answers=Answer.query.all()
    count=0
    context={
        'answers':answers,
        'count':count,
        'questions':questions,
    }
    return render_template('index.html',**context)

#create_an account
@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        
        full_name=request.form.get('full_name'),
        username=request.form.get('username'),
        email=request.form.get('email'),
        password=generate_password_hash(request.form.get('password'))
        user_in_existence=User.query.filter_by(email=email).first()

        if user_in_existence:
            flash("Account with email '%s' Already Exists"%email)
            return redirect(url_for('signup')) 
        
        args={
            'full_name':full_name,
            'username':username,
            'email':email,
            'password':password
        }
        
        new_user=User(**args)
        db.session.add(new_user)
        db.session.commit()
        flash('Account Has Been Created Successfully')
        return redirect(url_for('login'))
    return render_template('sign.html')

#sign in
@app.route('/login',methods=['GET', 'POST'])
def login():
    username=request.form.get('username')
    password=request.form.get('password')

    user=User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password,password):
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')

#sign out a user
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
    return redirect(url_for('index'))

#ask page
@app.route('/ask_questions')
def ask_page():
    return render_template('ask.html')

#view people's questions
@app.route('/feed')
def view_questions():
    questions=Question.query.order_by(Question.id.desc()).limit(10).all()
    count=0
    answers=Answer.query.all()
    for i in questions:
        for a in answers:
            if a.question_id == i.id:
                count+=1
               
    context={
        'answers':answers,
        'count':count,
        'questions':questions,
    }

  
                

    return render_template('stackfeed.html',**context)

#delete a question
@app.route('/delet  e_question/<int:question_id>',methods=['POST','GET'])
def delete_question(question_id):
    question_to_delete=Question.query.get_or_404(question_id)
    db.session.delete(question_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

##update a question
@app.route('/update_question/<int:question_id>',methods=['GET', 'POST'])
def update_question(question_id):
    question_to_update=Question.query.get_or_404(question_id)
    if request.method == 'POST':
        question_to_update.title=request.form.get('title')
        question_to_update.content=request.form.get('description')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html',question_to_update=question_to_update)

#answer a question
@app.route('/answer_question/<int:question_id>')
def answer_question(question_id):
    question_to_answer=Question.query.get_or_404(question_id)
    answers=Answer.query.filter_by(question=question_to_answer).all()
    count=0
    for i in answers:
        count+=1
    context={
    'question_to_answer':question_to_answer,
    'answers':answers,
    'count':count
    }

    return render_template('answer.html',**context)

@app.route('/add_answer/<int:question_id>',methods=['POST'])
def add_answer(question_id):
    question_to_answer=Question.query.get_or_404(question_id)
    content=request.form.get('content')
    args={
     'content':content,
     'author':current_user,
     'question':question_to_answer
    }
    new_answer=Answer(**args)
    db.session.add(new_answer)
    db.session.commit()
    return redirect(url_for('view_questions'))

@app.route('/delete_answer/<int:answer_id>')
def delete_answer(answer_id):
    answer_todelete=Answer.query.get_or_404(answer_id)
    db.session.delete(answer_todelete)
    db.session.commit()
    flash('Answer Removed')
    return redirect(url_for('index'))
