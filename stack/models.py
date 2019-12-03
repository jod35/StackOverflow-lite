from . import db,login_manager
from flask_login import UserMixin



class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    full_name=db.Column(db.String(40),nullable=False)
    username=db.Column(db.String(12),nullable=False,unique=True)
    email=db.Column(db.String(80),nullable=False,unique=True)
    password=db.Column(db.Text,nullable=False)
    questions=db.relationship('Question',backref='author',lazy=True)
    

    def __repr__(self):
        return "{}".format(self.full_name)

class Question(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(40),nullable=False)
    content =db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer(),db.ForeignKey('user.id'))
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))