__package__ = "application.views"

from .. import app,get_current_user
from ..database import get_db
from flask import render_template,redirect,url_for,session
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import StringField,PasswordField
from werkzeug.security import generate_password_hash, check_password_hash

class LoginForm(FlaskForm):
    username = StringField("Name",validators=[InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])

@app.route('/login',methods=["GET","POST"])
def login():
    user_details = get_current_user()
    user_error_message = None
    pass_error_message = None
    loginform = LoginForm()

    if loginform.validate_on_submit():
        username = loginform.username.data
        password = loginform.password.data
        hashed_password = generate_password_hash(password,method='sha256')
        db = get_db()
        c = db.execute('select id,name,password from users where name = ?',[username])
        user_result = c.fetchone()
        if user_result:
            app.logger.debug("User %s logged in !",user_result['name'])
            returned_password = user_result['password']
            if check_password_hash(returned_password,password):
                session['username'] = user_result['name']
                return redirect(url_for('index'))
            else:
                pass_error_message = "Passwords don't match"
                app.logger.error(pass_error_message)
        else:
            user_error_message = "User does not exist!"
            app.logger.error(user_error_message)

    return render_template('login.html',user=user_details,user_error=user_error_message,pass_error=pass_error_message,form=loginform)

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))