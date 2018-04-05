__package__ = "application.views"

from .. import app,get_current_user
from ..database import get_db
from flask import render_template,redirect,url_for

@app.route('/question/<question_id>')
def question(question_id):
    app.logger.debug("Retrieving information about question : %s",str(question_id))
    user_details = get_current_user()
    db = get_db()
    question_details_cur = db.execute('''
                                        select questions.question_text as question,
                                        questions.answer_text as answer,
                                        askers.name as asked_by,experts.name as expert
                                        from questions,users as askers,users as experts
                                        where questions.asked_by_id = askers.id 
                                        and questions.expert_id = experts.id 
                                        and questions.id = ?''',[question_id])
    details = question_details_cur.fetchall()
    return render_template('question.html',user=user_details,details=details)