__package__ = "application.views"

from .. import app,get_current_user
from ..database import get_db
from flask import render_template,redirect,url_for


@app.route('/users')
def users():
    user_details = get_current_user()
    if user_details:
        if user_details['admin'] == 1:
            app.logger.debug('Current user %s is an admin',user_details['name'])
            db = get_db()
            user_cur = db.execute('select id,name,expert,admin from users where admin != 1')
            users = user_cur.fetchall()
            return render_template('users.html',user=user_details,users=users)
        else:
            app.logger.debug('Current user %s is not an admin', user_details['name'])
            return redirect(url_for('index'))
    else:
        app.logger.debug('User not signed in !')
        return redirect(url_for('login'))

@app.route('/promote/<user_id>')
def promote(user_id):
    app.logger.debug("Attempting to promote/demote user with id : %s",str(user_id))
    user_details = get_current_user()
    if user_details:
        if user_details['admin'] == 1:
            app.logger.debug('Current user %s is an admin', user_details['name'])
            db = get_db()
            db.execute('update users set expert = case when expert = 1 then 0 else 1 end where id = ?',[user_id])
            db.commit()
            return redirect(url_for('users'))
        else:
            app.logger.debug('Current user %s is not an admin', user_details['name'])
            return redirect(url_for('index'))
    else:
        app.logger.debug('User not signed in !')
        return redirect(url_for('login'))
