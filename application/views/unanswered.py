__package__ = "application.views"

from .. import app,get_current_user
from ..database import get_db
from flask import render_template,redirect,url_for


@app.route('/unanswered')
def unanswered():
    user_details = get_current_user()
    if user_details:
        if user_details['expert'] == 1:
            app.logger.debug("Current user %s is an expert",user_details['name'])
            db = get_db()
            unanswered_cur = db.execute('''
                                            select questions.id,questions.question_text,users.name from questions , users
                                             where questions.expert_id = ? 
                                             and questions.asked_by_id = users.id
                                             and questions.answer_text is NULL ''',[user_details['id']])
            unanswered_questions = unanswered_cur.fetchall()
            return render_template('unanswered.html',user=user_details,questions=unanswered_questions)
        else:
            app.logger.debug("Current user %s is not an expert", user_details['name'])
            return redirect(url_for('index'))
    else:
        app.logger.debug("User not logged in !")
        return redirect(url_for('login'))