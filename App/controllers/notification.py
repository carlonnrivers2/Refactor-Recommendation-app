from App.models import Notification, Request_Recommendation
from App.database import db
from sqlalchemy.exc import IntegrityError
from App.controllers import get_user, check_expired_requests

def populate_notification(notif):
    if notif and notif.Request_Recommendation:
        notif.Student = get_user(notif.Request_Recommendation.studentID)
    return notif

# gets a notification from a user's notif feed
def get_staff_notifications(staffID):
    check_expired_requests()
    notifs = Notification.query.filter_by(staffID=staffID).all()

    for notif in notifs:
        notif = populate_notification(notif)
    
    return notifs

# gets a notification from a user's notif feed
def get_notification_by_request(reqID):
    check_expired_requests()
    notif = Notification.query.filter_by(reqID=reqID).first()
    notif = populate_notification(notif)

    return notif

def set_notification_seen(notif):
    notif.seen = True
    try:
        db.session.add(notif)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    return notif
