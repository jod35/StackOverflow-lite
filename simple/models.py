from . import db,login_manager
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(25),nullable=False,unique=True)
    email=db.Column(db.String(80),nullable=False,unique=True)
    password=db.Column(db.String(25),nullable=False)
    
    def __repr__(self):
        return "user {}".format(self.username)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

