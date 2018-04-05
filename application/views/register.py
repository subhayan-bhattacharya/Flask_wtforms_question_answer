__package__ = "application.views"

from .. import app,get_current_user
from ..database import get_db
from flask import render_template,redirect,url_for,session
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import StringField,PasswordField
from werkzeug.security import generate_password_hash, check_password_hash

class RegisterForm(FlaskForm):
    username = StringField("Name",validators=[InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])

@app.route('/register',methods=["GET","POST"])
def register():
    user_details = get_current_user()
    db = get_db()
    error_message = None
    registerform = RegisterForm()
    if registerform.validate_on_submit():
        app.logger.debug("Register form validated successfully !")
        username = registerform.username.data
        password = registerform.password.data
        app.logger.debug("User %s is wanting to be registered",username)
        existing_user_cur = db.execute('select count(*) as count from users where name = ?',[username])
        no = existing_user_cur.fetchone()
        if no['count'] == 0:
            hashed_password = generate_password_hash(password,method='sha256')
            db.execute('insert into users(name,password,expert,admin) values(?,?,?,?)',[username,hashed_password,'0','0'])
            db.commit()
            session['username'] = username
            app.logger.debug("Adding %s to session variable",username)
            return redirect(url_for('index'))
        else:
            error_message = "User already exists!"
            app.logger.debug("%s already exists in the database",username)

    return render_template('register.html',user=user_details,error=error_message,form=registerform)