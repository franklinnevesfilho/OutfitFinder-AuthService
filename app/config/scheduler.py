from apscheduler.schedulers.background import BackgroundScheduler
from app.models import RefreshToken
from datetime import datetime
from . import database

scheduler = BackgroundScheduler()

@scheduler.scheduled_job("interval", minutes=1)
def delete_expired_tokens():

    session = database.get_session()
    expired_tokens = session.query(RefreshToken).filter(RefreshToken.expires < datetime.now()).all()

    for token in expired_tokens:
        session.delete(token)

    session.commit()
    session.close()