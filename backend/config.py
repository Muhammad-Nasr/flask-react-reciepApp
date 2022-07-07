import os
base_url = os.path.dirname(os.path.realpath(__name__))
class Config:
    SECRET_KEY= os.environ.get('SECRETS_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    


class DevConfig(Config):
    

    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(base_url + 'dev.db')


class TestConfig(Config):
        SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
        TESTING= True
        JWT_SECRET_KEY='SECRET KEY'

