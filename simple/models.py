from . import db

class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(25),nullable=False,unique=True)
    email=db.Column(db.String(80),nullable=False,unique=True)
    password=db.Column(db.String(25),nullable=False,unique=True)
    
    def __repr__(self):
        return "user {}".format(self.username)
