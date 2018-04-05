__package__ = "application.views"

from .. import app,get_current_user
from ..database import get_db
from flask import render_template,redirect,url_for,session,request
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import TextAreaField,SelectField
from werkzeug.security import generate_password_hash, check_password_hash

def get_experts():
    app.logger.debug("Inside get_experts function")
    db = get_db()
    expert_cur = db.execute('select id,name from users where expert = 1 and admin = 0')
    experts = expert_cur.fetchall()
    expertlist = []
    for expert in experts:
        t = (str(expert['id']), expert['name'])
        expertlist.append(t)
    return expertlist


@app.route('/ask',methods=["GET","POST"])
def ask():
    app.logger.info("Inside ask route")
    db = get_db()
    user_details = get_current_user()

    class AskForm(FlaskForm):
        question = TextAreaField("Question",validators=[InputRequired()])
        expert = SelectField("Experts", choices=get_experts())

    askform = AskForm()

    if request.method == "POST":
        if askform.validate_on_submit():
            app.logger.debug("validation succeeded!")
            question = askform.question.data
            expert_id = askform.expert.data
            ask_by_id = user_details['id']
            db.execute('insert into questions(question_text,asked_by_id,expert_id) values(?,?,?)',[question,ask_by_id,int(expert_id)])
            db.commit()
            return redirect(url_for('index'))
        else:
            app.logger.error("Errors in validation %s",askform.errors)

    if user_details:
        app.logger.debug("User is logged in !")
        return render_template('ask.html',user=user_details,form=askform)
    else:
        app.logger.debug("User is not logged in !")
        return redirect(url_for('login'))



