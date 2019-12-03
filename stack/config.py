class DevConfig:
    my_password="nathanoj35"
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://jod35:{}@localhost/stack'.format(my_password)
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY='iamsecret'
    DEBUG=True
