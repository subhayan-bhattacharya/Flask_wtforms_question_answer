__package__ = "application.views"

from .. import app,get_current_user
from ..database import get_db
from flask import render_template,redirect,url_for,session
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired
from wtforms import TextAreaField
from werkzeug.security import generate_password_hash, check_password_hash

class AnswerForm(FlaskForm):
    answer = TextAreaField("Answer",validators=[InputRequired()])

@app.route('/answer/<question_id>',methods=["GET","POST"])
def answer(question_id):
    app.logger.info("Inside answer route with question id : %s \n",str(question_id))
    user_details = get_current_user()
    db = get_db()
    answerform = AnswerForm()

    if answerform.validate_on_submit():
        app.logger.debug("Answer form validated \n")
        answer = answerform.answer.data
        db.execute('update questions set answer_text = ? where id =?',[answer,question_id])
        db.commit()
        return redirect(url_for('unanswered'))

    if user_details:
        app.logger.debug("User %s logged in !",user_details['name'])
        if user_details['expert'] == 1:
            app.logger.debug("user %s is an expert",user_details['name'])
            question_cur = db.execute('select id,question_text from questions where id = ?',[question_id])
            question = question_cur.fetchone()
            return render_template('answer.html',user=user_details,question=question,form=answerform)
        else:
            app.logger.debug("user %s is not an expert", user_details['name'])
            return redirect(url_for('index'))
    else:
        app.logger.debug("User not logged in!")
        return redirect(url_for('login'))