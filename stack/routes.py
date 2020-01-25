from . import app,db,bcrypt
from flask import render_template,redirect,request,url_for,flash
from flask_login import login_user,logout_user,current_user
from .models import User,Question,Answer

#home page
@app.route('/')
def index():
    questions=Question.query.all()

    return render_template('index.html',questions=questions)

#create_an account
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

#sign in
@app.route('/login',methods=['GET', 'POST'])
def login():
    username=request.form.get('username')
    password=request.form.get('password')

    user=User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password,password):
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
    questions=Question.query.limit(10).all()
    return render_template('stackfeed.html',questions=questions)

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
    new_answer=Answer(content=content,question=question_to_answer,author=current_user)
    db.session.add(new_answer)
    db.session.commit()
    return redirect(url_for('view_questions'))
