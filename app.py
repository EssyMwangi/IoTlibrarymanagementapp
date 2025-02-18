"""This is file contains the application factory that contains necessary functions for the app to start.
It also contains necessary inititalizations for the app.This function is run by WSGI to start our application on the web."""
from flask import Flask
from views import routes
from extensions import db,admin,encrypt
from flask_login import LoginManager
from models import User
from config import SECRET_KEY, PASSWORD
import os
from admin import bp as admin_bp

#The application factory
def create_app(settings="config.py"):
    """Factory function to start the web app when everthing(i.e configurations are set up in place.)"""
    myapp=Flask(__name__)#Creating app instance
    myapp.config["SECRET_KEY"]=SECRET_KEY
    myapp.config["SQLALCHEMY_DATABASE_URI"]='mysql+pymysql://soupnazi:librarysystem@soupnazi.mysql.pythonanywhere-services.com/soupnazi$lib_data'
    myapp.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    myapp.config['SQLALCHEMY_POOL_RECYCLE'] = 299
    myapp.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
    DEBUG=False


    """Initializing extensions"""
    db.init_app(myapp)

    from models import User, Book
    with myapp.app_context():
        db.create_all()
        db.session.commit()

    admin.init_app(myapp)#The administrators instance
    encrypt.init_app(myapp)#Instance of bcrypt password hashing utility
    #client.on_connect=on_connect
    #client.on_message=on_message
    #client.connect('broker.hivemq.com', 1883)
    #client.loop_forever()


    #Registering routes
    myapp.register_blueprint(routes)
    myapp.register_blueprint(admin_bp)


    #Managing logins
    login_manager = LoginManager()
    login_manager.login_view = 'routes.login'
    login_manager.init_app(myapp)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return myapp

