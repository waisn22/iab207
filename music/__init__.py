#from package import Class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()

def create_app():
  
    app=Flask(__name__)  
    app.debug=True
    app.secret_key='somesecretgoeshere'
    
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mydbname.sqlite'
    
    db.init_app(app)

    bootstrap = Bootstrap5(app)
    
    login_manager = LoginManager()
    
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    
    from .models import User  
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.authbp)

    from . import events
    app.register_blueprint(events.eventbp)

    from . import users
    app.register_blueprint(users.userbp)

    @app.errorhandler(404) 
    
    def not_found(e): 
      return render_template("404.html", error=e)

    
    return app



