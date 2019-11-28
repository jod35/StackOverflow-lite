mydb_username='jod35'
mydb_password='nathanoj35'
class DevConfig:
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://{}:{}@localhost/simple'.format(mydb_username,mydb_password)
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY='notasecret'
    DEBUG=True