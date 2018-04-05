__package__ = "application.views"

from .. import app,get_current_user
from ..database import get_db
from flask import render_template,redirect,url_for

@app.route('/')
def index():
    app.logger.debug("Inside index route")
    user_details = get_current_user()
    db = get_db()
    results_cur = db.execute('''
                                select questions.id as id,questions.question_text as question,
                                askers.name as asked_by,experts.name as expert 
                                from questions,users as askers,
                                users as experts 
                                where questions.asked_by_id = askers.id
                                and questions.expert_id = experts.id
                                and questions.answer_text is not null
                                ''')
    results = results_cur.fetchall()
    app.logger.debug("Exiting index route")
    return render_template('home.html',user=user_details,results=results)

