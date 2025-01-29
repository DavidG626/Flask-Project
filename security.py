from functools import wraps
from flask import session, redirect, url_for
from datetime import datetime, timedelta

def check_session_timeout(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if user is not logged in or session has expired
        if 'user_id' not in session or 'last_active' not in session:
            return redirect(url_for('login_register.login'))
        
        # Check for session timeout (30 minutes)
        last_active = datetime.strptime(session['last_active'], '%Y-%m-%d %H:%M:%S.%f')
        if datetime.now() - last_active > timedelta(minutes=30):
            session.clear()
            return redirect(url_for('login_register.login'))
        
        # Update last active timestamp
        session['last_active'] = str(datetime.now())
        return func(*args, **kwargs)
    return wrapper