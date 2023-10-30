from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required, logout_user
from . import db


authbp = Blueprint('auth', __name__)

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    
    if (register.validate_on_submit()==True):
            
            uname = register.user_name.data
            pwd = register.password.data
            email = register.email_id.data
            
            user = db.session.scalar(db.select(User).where(User.name==uname))
            if user:
                flash('Username already exists, please try another')
                return redirect(url_for('auth.register'))
            
            pwd_hash = generate_password_hash(pwd)
            
            new_user = User(name=uname, password_hash=pwd_hash, emailid=email)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for('main.index'))
    #the else is called when the HTTP request calling this page is a GET
    else:
        return render_template('event/forms.html', form=register, heading='Register')
    

@authbp.route('/login', methods = ['GET', 'POST'])
def login():
  login = LoginForm()
  error=None
  if(login.validate_on_submit()):
    user_name = login.user_name.data
    password = login.password.data
    u1 = User.query.filter_by(name=user_name).first()
    
        #if there is no user with that name
    if u1 is None:
      error='Incorrect user name'
    #check the password - notice password hash function
    elif not check_password_hash(u1.password_hash, password): # takes the hash and password
      error='Incorrect password'
    if error is None:
    #all good, set the login_user
      login_user(u1)
      return redirect(url_for('main.index'))
    else:
      print(error)
      flash(error)
    #it comes here when it is a get method
  return render_template('event/forms.html', form=login, heading='Login')

@authbp.route('/logout')
def logout():
  logout_user()
  return 'Successfully logged out user'
